import collections
import numpy as np
import math
from scipy.signal import medfilt


def dispatch_function(filter_config_info, data_dict_input, config_info=None):
    match_item = filter_config_info["function"]
    # print(f"Dispatched function name: {match_item}")
    if match_item == 'cdp_direction':
        # t = data_dict_input[filter_config_info["input"]]
        # # need to be fixed ********
        # keyname = "need to be fixed"
        # f = cdp_direction(config_info.log, keyname, t)
        # data_dict_input[filter_config_info["output"]] = f
        print(f"{match_item} will be coming soon.")

    elif match_item == 'reduce':
        print(f"{match_item} will be coming soon.")
        # print('reduce')

    elif match_item == 'dwnsample':
        target_data = data_dict_input[filter_config_info["input"]]
        target_samplerate = filter_config_info["target_samplerate"]
        if len(target_data) > target_samplerate:
            diff_mean = np.nanmean(np.diff(target_data))
            estimated_samplerate = 1 / diff_mean
            approximated_reduction = math.log(math.floor(estimated_samplerate / target_samplerate), 2)
        else:
            approximated_reduction = 0

        # print(f"Target samplerate       =  {target_samplerate}")
        # print(f"Estimated samplerate    =  {estimated_samplerate}")
        # print(f"Approximated reductions =  {approximated_reduction}")

        if approximated_reduction == 0:
            return data_dict_input

        p = dwnsample(data_dict_input, approximated_reduction)
        data_dict_input = p
        return data_dict_input

    elif match_item == 'detectblinkV':
        x1 = data_dict_input[filter_config_info["input"][0]]
        x2 = data_dict_input[filter_config_info["input"][1]]
        x1 = medfilt(x1, 3)
        x2 = medfilt(x2, 3)

        # print(f"x1: {x1}")
        # print(f"x2: {x2}")

    elif match_item == 'deblinker2':
        x0 = data_dict_input[filter_config_info["input"][0]]
        y0 = data_dict_input[filter_config_info["input"][1]]
        th = filter_config_info["threshold"]

        i = deblinker2(x0, y0, th)
        data_dict_input[filter_config_info["output"]] = i

    elif match_item == 'passthrough':
        f = data_dict_input[filter_config_info["input"]]
        output_column = filter_config_info["output"]
        data_dict_input[output_column] = f
        # print(f"{output_column} column has been added to output data.")

    elif match_item == 'dshift':
        f = data_dict_input[filter_config_info["input"][0]]
        data_dict_input[filter_config_info["output"]] = dshift(f)

    elif match_item == 'tidy':
        f = data_dict_input[filter_config_info["input"][0]]
        n = filter_config_info["value"]
        thicken = filter_config_info["thicken"]

        is_tracking = data_dict_input[filter_config_info["input"][1]]
        data_dict_input[filter_config_info["output"]] = tidy(f, n, thicken, np.logical_not(is_tracking))

    elif match_item == 'wavelet':
        f = data_dict_input[filter_config_info["input"][0]]
        if are_all_elements_nan(f):
            data_dict_input[filter_config_info["output"]] = f
            return

        level_for_reconstruction = np.array(filter_config_info["levelForReconstruction"])
        wavelet_type = filter_config_info["type"]
        level = filter_config_info["Level"]
        data_dict_input[filter_config_info["output"]] = waveleter(f, level_for_reconstruction, wavelet_type, level)

    elif match_item == 'spikeRemover':
        print(f"{match_item} will be coming soon.")

    elif match_item == 'deblinker':
        print(f"{match_item} will be coming soon.")

    elif match_item == 'shiftSignal':
        print(f"{match_item} will be coming soon.")

    elif match_item == 'medianFilter':
        input_column = filter_config_info["input"][0]
        f = data_dict_input[input_column]
        n = filter_config_info["npoint"]
        if len(f) >= n:
            data_dict_input[filter_config_info["output"]] = medfilt(f, n)
        else:
            return data_dict_input
        # print(f"{input_column} column has been median filtered with n point {n}.")

    elif match_item == 'replaceNanBy':
        input_column = filter_config_info["input"][0]
        input_array = data_dict_input[input_column]
        pointer = filter_config_info["pointer"]
        data_dict_input[filter_config_info["output"]] = replace_nan_by(data_dict_input, input_array, pointer)

    elif match_item == 'applymask':
        print(f"{match_item} will be coming soon.")

    elif match_item == 'detrender':
        print(f"{match_item} will be coming soon.")

    elif match_item == 'detectblinkV':
        print(f"{match_item} will be coming soon.")

    elif match_item == 'gradient':
        related_column_name_array = filter_config_info["input"]
        f = data_dict_input[related_column_name_array[1]]
        t = data_dict_input[related_column_name_array[0]]
        output_column = filter_config_info["output"]
        data_dict_input[output_column] = grad(f, t)
        # print(f"{output_column} column is added to the output data by using gradient.")

    else:
        print(f"Function:{match_item} is not found")

    return data_dict_input


# def spike_remover(f):
#     pass


# def xdetectblink(x1, V, fps, varargin):
#     pass


# def detectblinkV(t, V, fps, varargin):
#     pass


def dwnsample(dict_input, number_of_reduction):
    f = len(dict_input[next(iter(dict_input))])
    print("********************", f)
    number_of_reduction = int(number_of_reduction)
    if isinstance(number_of_reduction, int):
        loop_count = 0
        while loop_count < number_of_reduction:
            loop_count += 1
            for key in dict_input:
                temp_array = dict_input[key]
                temp_array = temp_array[0:f:2]
                dict_input[key] = temp_array
    else:
        print("The number of loop input must be number!")

    return dict_input


def replace_nan_by(y, input_array, pointer):
    if "<=" in pointer:
        try:
            column_name, value = str(pointer).split("<=")
            pointer_column__array = y[column_name]
            array_length = len(input_array)
            for ind in range(array_length):
                if float(pointer_column__array[ind]) <= float(value):
                    input_array[ind] = np.nan
        except KeyError:
            pass
    elif "==" in pointer:
        try:
            column_name, value = str(pointer).split("==")
            pointer_column__array = y[column_name]
            array_length = len(input_array)
            for ind in range(array_length):
                if float(pointer_column__array[ind]) == float(value):
                    input_array[ind] = np.nan
        except KeyError:
            pass
    elif ">=" in pointer:
        try:
            column_name, value = str(pointer).split(">=")
            pointer_column__array = y[column_name]
            array_length = len(input_array)
            for ind in range(array_length):
                if float(pointer_column__array[ind]) >= float(value):
                    input_array[ind] = np.nan
        except KeyError:
            pass
    else:
        if ">" in pointer:
            try:
                column_name, value = str(pointer).split(">")
                pointer_column__array = y[column_name]
                array_length = len(input_array)
                for ind in range(array_length):
                    if float(pointer_column__array[ind]) > float(value):
                        input_array[ind] = np.nan
            except KeyError:
                pass
        elif "<" in pointer:
            try:
                column_name, value = str(pointer).split("<")
                pointer_column__array = y[column_name]
                array_length = len(input_array)
                for ind in range(array_length):
                    if float(pointer_column__array[ind]) < float(value):
                        input_array[ind] = np.nan
            except KeyError:
                pass
        else:
            pass

    return input_array


def waveleter(x, level_for_reconstruction, wavelet_type, level):
    [x1, i] = fillmissing(x)
    x11 = x1

    return x11


def deblinker2(x, y, th):
    s = x * y
    i = (s > th)
    return i


def applymask(f, is_mask):
    pass


def deblinker(f, is_blinking):
    pass


def medianfilter(f, npoint):
    pass


def tidy(f, npoint, n_thicken, is_deleted):
    # need  to be fixed
    return f


def dshift(f):
    y = np.nanmean(f)
    f1 = f - y
    return f1


def grad(f, t):

    try:
        df = np.gradient(f)
        dt = np.gradient(t)
        dfdt = df / dt
        print("dfdt", dfdt)
        for ind, value in enumerate(dfdt):
            if math.isinf(value):
                dfdt[ind] = 0
            if np.isnan(value):
                dfdt[ind] = 0
        return dfdt
    except ValueError:
        return 0
    except RuntimeWarning:
        return 0


def cdp_direction(logs, fname, t):
    return t


# def medfilt1(x, k):
#     # Apply a length-k median filter to a 1D array x.
#     # Boundaries are extended by repeating endpoints.
#     assert k % 2 == 1, "Median filter length must be odd."
#     assert x.ndim == 1, "Input must be one-dimensional."
#     k2 = (k - 1) // 2
#     data_dict_input = np.zeros((len(x), k), dtype=x.dtype)
#     data_dict_input[:, k2] = x
#     for i in range(k2):
#         j = k2 - i
#         data_dict_input[j:, i] = x[:-j]
#         data_dict_input[:j, i] = x[0]
#         data_dict_input[:-j, -(i + 1)] = x[j:]
#         data_dict_input[-j:, -(i + 1)] = x[-1]
#     return np.median(data_dict_input, axis=1)

def are_all_elements_nan(input_array):
    for ele in input_array:
        if not np.isnan(ele):
            return False
    return True


def fillmissing(input_array):
    # input_array = ma.masked_array(input_array, input_array == np.nan)
    # for shift in (-1, 1):
    #     for axis in (0, 1):
    #         shifted_array = np.roll(input_array, shift=shift, axis=axis)
    #         idx = ~shifted_array.mask * input_array.mask
    #         input_array[idx] = shifted_array[idx]
    return input_array


class Updater:
    def __init__(self, config, circular_buffer, header_array):
        if type(config) is not dict:
            raise ValueError("The config input must be dictionary type.")
        if type(circular_buffer) is not collections.deque:
            raise ValueError("The circular_buffer input must be collections.deque type.")
        if type(header_array) is not list:
            raise ValueError("The circular_buffer input must be list type.")
        if not header_array:
            raise ValueError("The header_array input must not be empty.")
        for header in header_array:
            if type(header) is not str:
                raise ValueError("The header_array element must be string.")
        self.config = config
        self.circular_buffer = circular_buffer
        self.buffer_max_length = circular_buffer.maxlen
        self.header_array = header_array

    def update(self, data_input):
        self.circular_buffer.append(data_input)
        data_dict = {}
        output_header_array = [header for header in self.header_array]
        output_data = []
        filter_config = self.config["filters"]
        for filter_info in filter_config:
            if filter_info["Enabled"]:
                try:
                    output_header = filter_info["output"]
                except KeyError:
                    output_header = None
                if output_header and output_header not in output_header_array:
                    output_header_array.append(output_header)
        for header in self.header_array:
            data_dict[header] = []
        for data in self.circular_buffer:
            for header_index, header_string in enumerate(self.header_array):
                data_dict[header_string].append(float(data[header_index]))

        # if len(self.circular_buffer) >= 3:
        for filter_info in filter_config:
            if filter_info["Enabled"]:
                data_dict = dispatch_function(filter_info, data_dict, self.config)
            else:
                pass

        for index in range(len(data_dict[output_header_array[0]])):
            temp_array = []
            for header in output_header_array:
                try:
                    temp_array.append(data_dict[header][index])
                except TypeError:
                    temp_array.append(0)
            output_data.append(temp_array)
            # len_diff = len(output_header_array) - len(self.header_array)
            # for data in self.circular_buffer:
            #     temp_array = [ele for ele in data]
            #     temp_array.extend(len_diff * [0])
            #     output_data.append(temp_array)

        # print("output_data")
        # for d in output_data:
        #     print(d)
        # print("end")
        return output_data[-1]

    def set_config(self, new_config):
        if type(new_config) is not dict:
            raise ValueError("The config input must be dictionary type.")
        self.config = new_config

    def set_buffer(self, new_buffer):
        if type(new_buffer) is not collections.deque:
            raise ValueError("The circular_buffer input must be collections.deque type.")
        self.circular_buffer = new_buffer
        self.buffer_max_length = new_buffer.maxlen
    # # This function is to get header position from the given array
    # def get_index(search_input, array_in):
    #     idx_found = False
    #     return_idx = None
    #     for idx, val in enumerate(array_in):
    #         if val == search_input:
    #             idx_found = True
    #             return_idx = idx
    #             break
    #
    #     if not idx_found:
    #         print(f"{search_input} can not be found!")
    #
    #     return return_idx
    #
    #
    # # The main function to preprocess the csv data
    # # This function is also the translation of matlab run_updater function from the okn_matlab repo
    # def run_updater(config, inputfile, outputfile, varargin=None):
    #     start_time = time.time()
    #     if varargin is not None:
    #         print("varargin is not none.")
    #     data_table = None
    #     row_count = None
    #
    #     if isinstance(config, str):
    #         config = load_commented_json(config)
    #
    #     if isinstance(inputfile, str):
    #         data_table = read_table(inputfile)
    #
    #     # extra information
    #     extra = {"inputfile": inputfile, "outputfile": outputfile, "config": config}
    #
    #     config_filter_info_array = config["filters"]
    #
    #     for filter_info in config_filter_info_array:
    #         if filter_info["Enabled"]:
    #             data_table = dispatch_function(filter_info, data_table, extra)
    #         else:
    #             pass
    #
    #     header_array = []
    #     for key in data_table:
    #         header_array.append(key)
    #
    #     print("Start updating the csv!")
    #     with open(outputfile, mode='w', newline="") as destination_file:
    #         csv_writer = csv.DictWriter(destination_file, fieldnames=header_array)
    #         csv_writer.writeheader()
    #
    #         row_count = len(data_table[header_array[0]])
    #
    #         for i in range(row_count):
    #             temp_dict = {}
    #             for header in header_array:
    #                 temp_dict[header] = data_table[header][i]
    #             csv_writer.writerow(temp_dict)
    #     print(f"csv is updated and it took {time.time() - start_time} sec")
    #     print("--------------------------------------------------------------------------------------")
    #     return outputfile
    #
    #
    # ###########################################################
    # # FILTER DISPATCHER
    # ###########################################################
    #
    # dispatch function
