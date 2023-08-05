import os.path
import sys

import pandas as pd

from lm_datahandler.data_download.data_download import download_lm_data_from_server
from lm_datahandler.datahandler import DataHandler
import scipy.signal as sp_sig
import numpy as np
from scipy.integrate._quadrature import simps


def download_and_full_analyse(download_params):
    data_save_path = download_params["save_path"]
    data_list = download_lm_data_from_server(download_params, data_save_path)

    analysis_save_path = download_params["analysis_save_path"]

    show_plots = download_params["show_plots"]

    local_datas_full_analyse(data_save_path, data_list, analysis_save_path=analysis_save_path, show_plots=show_plots)


def local_datas_full_analyse(data_path, data_names, analysis_save_path=None, show_plots=False):
    assert os.path.exists(data_path), "The input dir path does not exist."

    if analysis_save_path is None:
        analysis_save_path = data_path
    else:
        if not os.path.exists(analysis_save_path):
            os.mkdir(analysis_save_path)
    for i, data_name in enumerate(data_names):
        print("Start analysis data: {}".format(data_name))
        if not os.path.exists(os.path.join(data_path, data_name)):
            print("data: \"{}\" not found, skipped.".format(data_name))
            continue
        try:

            data_handler = DataHandler()

            temp_data_path = os.path.join(data_path, data_name)

            data_analysis_save_path = os.path.join(analysis_save_path, data_name)

            if not os.path.exists(data_analysis_save_path):
                os.mkdir(data_analysis_save_path)
            sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")
            slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

            analysis_results_save_path = os.path.join(data_analysis_save_path, "analysis_results.xlsx")

            analysis_report_save_path = os.path.join(data_analysis_save_path, data_name+"_sleep_report.pdf")

            # 数据加载
            patient_info = {"phone_number": data_name[0:11]}
            data_handler.load_data(data_name=data_name, data_path=temp_data_path, patient_info=patient_info)

            # 绘制慢波增强对比图，并保存
            data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

            # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
            data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [
                [49, 51]]}).sleep_staging().compute_sleep_variables().plot_sleep_data(
                savefig=sleep_fig_save_path)

            # data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': 70, 'bandstop': [
            #     [49, 51]]}).sleep_staging().compute_sleep_variables()

            # features = generate_cluster_feature(data_handler)
            # features_df = pd.DataFrame(features)
            # features_df.to_csv(os.path.join(data_analysis_save_path, "cluster_features.csv"), index=True)

            # spindle检测和慢波检测
            data_handler.sw_detect().spindle_detect()

            # 导出结果成excel
            data_handler.export_analysis_result_to_xlsx(analysis_results_save_path, sw_results=True, sp_results=True,
                                                        sleep_variables=True)

            if show_plots:
                data_handler.show_plots()

            data_handler.export_analysis_report(analysis_report_save_path)


        except AssertionError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("AssertionError: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Unknown Error: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        finally:

            continue

def local_data_concat_and_analyse(data_path, data_names, analysis_save_path=None, show_plots=False):
    assert os.path.exists(data_path), "The input dir path does not exist."

    data_handler = DataHandler()

    for i in range(len(data_names)):
        # 数据加载
        if i == 0:
            patient_info = {"phone_number": data_names[i][0:11]}
            data_handler.load_data(data_name=data_names[0], data_path=os.path.join(data_path, data_names[i]), patient_info=patient_info)
        else:
            data_handler.concat_data(data_path=os.path.join(data_path, data_names[i]))

    data_name = data_handler.data_name

    data_analysis_save_path = os.path.join(analysis_save_path, data_name)

    if not os.path.exists(data_analysis_save_path):
        os.mkdir(data_analysis_save_path)
    sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")
    slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

    analysis_results_save_path = os.path.join(data_analysis_save_path, "analysis_results.xlsx")

    analysis_report_save_path = os.path.join(data_analysis_save_path, "sleep_report.pdf")



    # 绘制慢波增强对比图，并保存
    data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

    # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
    data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': 70, 'bandstop': [
        [49, 51]]}).sleep_staging().compute_sleep_variables().plot_sleep_data(
        savefig=sleep_fig_save_path)

    # data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': 70, 'bandstop': [
    #     [49, 51]]}).sleep_staging().compute_sleep_variables()

    # features = generate_cluster_feature(data_handler)
    # features_df = pd.DataFrame(features)
    # features_df.to_csv(os.path.join(data_analysis_save_path, "cluster_features.csv"), index=True)

    # spindle检测和慢波检测
    data_handler.sw_detect().spindle_detect()


    # 导出结果成excel
    data_handler.export_analysis_result_to_xlsx(analysis_results_save_path, sw_results=True, sp_results=True,
                                                sleep_variables=True)

    if show_plots:
        data_handler.show_plots()

    data_handler.export_analysis_report(analysis_report_save_path)


def compute_sleep_variables_from_hypno(hypno):
    data_handler = DataHandler()
    data_handler.compute_sleep_variables(hypno)
    sleep_variables_df = {
        "TST(H)": [data_handler.sleep_variables["TST"] / 3600],
        "SOL(H)": [data_handler.sleep_variables["SOL"] / 3600],
        "GU(H)": [data_handler.sleep_variables["GU"] / 3600],
        "WASO(M)": [data_handler.sleep_variables["WASO"] / 60],
        "SE(%)": [data_handler.sleep_variables["SE"] * 100],
        "AR": [data_handler.sleep_variables["AR"]],
        "N3(H)": [data_handler.sleep_variables["N3"] / 3600],
        "N12(H)": [data_handler.sleep_variables["N12"] / 3600],
        "REM(H)": [data_handler.sleep_variables["REM"] / 3600],
        "Hypno": [data_handler.sleep_variables["HYPNO"]]
    }
    print(sleep_variables_df)


def bandpower_from_psd_ndarray(bands, psd, freqs, relative=True):
    # Type checks
    assert isinstance(bands, list), "bands must be a list of tuple(s)"
    assert isinstance(relative, bool), "relative must be a boolean"

    # Safety checks
    freqs = np.asarray(freqs)
    psd = np.asarray(psd)
    assert freqs.ndim == 1, "freqs must be a 1-D array of shape (n_freqs,)"
    assert psd.shape[-1] == freqs.shape[-1], "n_freqs must be last axis of psd"

    # Extract frequencies of interest
    all_freqs = np.hstack([[b[0], b[1]] for b in bands])
    fmin, fmax = min(all_freqs), max(all_freqs)
    idx_good_freq = np.logical_and(freqs >= fmin, freqs <= fmax)
    freqs = freqs[idx_good_freq]
    res = freqs[1] - freqs[0]

    # Trim PSD to frequencies of interest
    psd = psd[..., idx_good_freq]

    # plt.imshow(psd.T[:50,:], cmap='jet')
    # plt.show()
    # assert 0

    # Check if there are negative values in PSD
    if (psd < 0).any():
        pass

    # Calculate total power
    total_power = simps(psd, dx=res, axis=-1)
    total_power = total_power[np.newaxis, ...]

    # Initialize empty array
    bp = np.zeros((len(bands), *psd.shape[:-1]), dtype=np.float64)

    # Enumerate over the frequency bands
    labels = []
    for i, band in enumerate(bands):
        b0, b1, la = band
        labels.append(la)
        idx_band = np.logical_and(freqs >= b0, freqs <= b1)
        bp[i] = simps(psd[..., idx_band], dx=res, axis=-1)

    if relative:
        bp /= total_power

    all_freqs = all_freqs.reshape(-1, 2)
    total_bands = all_freqs[:, 1] - all_freqs[:, 0]
    total_bands = total_bands[..., np.newaxis]
    bp /= total_bands
    return bp


def generate_cluster_feature(data_handler):
    epochs = data_handler.eeg.shape[0] // (data_handler.sf_eeg * data_handler.epoch_len)
    input_eeg = data_handler.eeg[0:epochs * data_handler.sf_eeg * data_handler.epoch_len].reshape(-1,
                                                                                                  data_handler.sf_eeg * data_handler.epoch_len)

    hypno = data_handler.sleep_staging_result
    n3_index = np.where(hypno == 0)
    n12_index = np.where(hypno == 1)

    bands = [
        (1, 4, "delta"),
        (4, 8, "theta"),
        (8, 13, "alpha"),
        (11, 16, "spindle"),
        (16, 30, "beta"),
        (30, 40, "gamma"),
    ]

    win = int(5 * 500)
    kwargs_welch = dict(window="hamming", nperseg=win, average="median")
    freqs, psd = sp_sig.welch(input_eeg, 500, **kwargs_welch)

    n3_psd = psd[n3_index]
    n12_psd = psd[n12_index]

    n3_percentile_10 = np.percentile(n3_psd, 10, axis=0)
    n3_percentile_90 = np.percentile(n3_psd, 90, axis=0)
    n3_psd_new = []
    for i in range(n3_psd.shape[0]):
        temp = n3_psd[i, :]
        temp[temp < n3_percentile_10] = n3_percentile_10[temp < n3_percentile_10]
        temp[temp > n3_percentile_90] = n3_percentile_90[temp > n3_percentile_90]
        n3_psd_new.append(temp)
    n3_psd = np.asarray(n3_psd_new)

    n12_percentile_10 = np.percentile(n12_psd, 10, axis=0)
    n12_percentile_90 = np.percentile(n12_psd, 90, axis=0)
    n12_psd_new = []
    for i in range(n12_psd.shape[0]):
        temp = n12_psd[i, :]
        temp[temp < n12_percentile_10] = n12_percentile_10[temp < n12_percentile_10]
        temp[temp > n12_percentile_90] = n12_percentile_90[temp > n12_percentile_90]
        n12_psd_new.append(temp)
    n12_psd = np.asarray(n12_psd_new)

    n3_psd_avg = np.average(n3_psd, axis=0)
    n12_psd_avg = np.average(n12_psd, axis=0)

    n3_psd_avg_beta = np.sum(np.reshape(n3_psd_avg[16 * 5:30 * 5], [-1, 5]), axis=1)
    n3_psd_avg_alpha = np.sum(np.reshape(n3_psd_avg[8 * 5:13 * 5], [-1, 5]), axis=1)
    n3_psd_avg_delta = np.sum(np.reshape(n3_psd_avg[1 * 5:4 * 5], [-1, 5]), axis=1)

    n12_psd_avg_delta = np.sum(np.reshape(n12_psd_avg[1 * 5:4 * 5], [-1, 5]), axis=1)
    n12_psd_avg_beta = np.sum(np.reshape(n12_psd_avg[16 * 5:30 * 5], [-1, 5]), axis=1)
    n12_psd_avg_alpha = np.sum(np.reshape(n12_psd_avg[8 * 5:13 * 5], [-1, 5]), axis=1)

    fmax_n3_beta = np.argmax(n3_psd_avg_beta)+16
    fmax_n3_alpha = np.argmax(n3_psd_avg_alpha)+8
    fmax_n12_delta = np.argmax(n12_psd_avg_delta)+1

    pmax_n3_delta = np.max(n3_psd_avg_delta)
    pmax_n3_beta = np.max(n3_psd_avg_beta)
    pmax_n3_alpha = np.max(n3_psd_avg_alpha)

    pmax_n12_beta = np.max(n12_psd_avg_beta)
    pmax_n12_alpha = np.max(n12_psd_avg_alpha)

    return {'fmax_n3_beta': [fmax_n3_beta],
            'fmax_n3_alpha': [fmax_n3_alpha],
            'fmax_n12_delta': [fmax_n12_delta],
            'pmax_n3_delta': [pmax_n3_delta],
            'pmax_n3_beta': [pmax_n3_beta],
            'pmax_n3_alpha': [pmax_n3_alpha],
            'pmax_n12_beta': [pmax_n12_beta],
            'pmax_n12_alpha': [pmax_n12_alpha]}


if __name__ == '__main__':
    # day = '20230726'
    # download_param = {
    #     # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
    #     'paradigms': None,
    #     # 用户手机号
    #     'phones': [15167196173],
    #     # 基座mac
    #     'macs': None,
    #     # 服务版本
    #     'serviceVersions': None,
    #     # 睡眠主观评分，1~5，-1表示未评分
    #     'sleepScores': None,
    #     # 停止类型， 0. 断连超时, 1. 用户手动, 2. 头贴放到基座上停止, 3. 关机指令触发, 4. 低电量, 5. 崩溃
    #     'stopTypes': None,
    #     # 时间范围，以停止记录的时间为准
    #     'dateRange': ['20230726', '20230726'],
    #     # 数据时长范围
    #     'dataLengthRange': [60 * 5, 60 * 12],
    #     # 翻身次数范围
    #     'turnoverCountRange': None,
    #     # 刺激次数范围
    #     'stimulationCountRange': None,
    #     # 下载保存路径
    #     'save_path': os.path.join('E:/dataset/x7_data_by_days/data', day),
    #     # 分析结果保存路径（为None表示保存在数据下载路径中）
    #     'analysis_save_path': os.path.join('E:/dataset/x7_data_by_days/analysis', day),
    #     'show_plots': True
    # }
    # download_and_full_analyse(download_param)

    # data_paths = r'E:\dataset\x7_addiction\20230727_20230801'
    # for j in os.listdir(data_paths):
    #     data_path = os.path.join(data_paths, j)
    #     data_names = []
    #     for i in os.listdir(data_path):
    #         if os.path.isdir(os.path.join(data_path, i)):
    #             data_names.append(i)
    #
    #     # data_names = [
    #     #               '15121122284_0725-09_08_04_0725-13_30_19_0.00_5',
    #     #             ]
    #     analysis_result_save_path = os.path.join(r'E:\dataset\x7_addiction\20230727_20230801', j)
    #     local_datas_full_analyse(data_path, data_names, analysis_result_save_path, show_plots=False)

    # local_datas_full_analyse(r'C:\Users\DELL\Downloads',
    #                          ["15221269950_0728-23_30_41_0729-06_26_11_0.00_4"],
    #                          r'C:\Users\DELL\Downloads', show_plots=False)

    data_paths = r'E:\dataset\dev_test_data\dev_server_data'
    data_names = []
    for i in os.listdir(data_paths):
        if os.path.isdir(os.path.join(data_paths, i)):
            data_names.append(i)

    data_names = [
                  '15295795607_0705-00_01_05_0705-07_40_38_0.24_4',
                ]
    local_datas_full_analyse(data_paths, data_names, r'E:\dataset\dev_test_data\dev_server_data', show_plots=False)


    # data_paths = r'E:\dataset\dev_test_data\15921862148_0801'
    # data_names = []
    # for i in os.listdir(data_paths):
    #     if os.path.isdir(os.path.join(data_paths, i)):
    #         data_names.append(i)
    #
    # data_names = [
    #     '15921862148_0801-22_51_13_0802-01_24_28_0.00_4',
    #     '15921862148_0802-01_27_10_0802-06_44_22_0.00_4'
    # ]
    # local_data_concat_and_analyse(data_paths, data_names, r'E:\dataset\dev_test_data\15921862148_0801',
    #                          show_plots=False)
