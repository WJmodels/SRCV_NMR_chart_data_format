'''
修改SRCV输出谱图数据格式
cli 命令行接口 形如

python srcv_out_format.py './in/brackets - 副本.txt' './out/test2.txt'

'''
#import os
import fire




def format_out_line1(integral_range, area, peaks):
    peaks_str = ','.join([str(x) for x in peaks])
    return f'{{integral_range: ({integral_range[0]}, {integral_range[1]}), integral_area: {area}, peak: [{peaks_str}]}}'


def parse_segs(lines_src):
    ''' 
    不同文件的段落出现顺序可能不同
    integral---------------------------------------------------

    shift--------------------------------------------------
    '''
    #get_segs
    seg_begin = False
    segs = []

    for line in lines_src:

        if line == '':
            #段间空行
            continue
        elif line[-1] == '-':
            if line[0] != '-' :
                seg_begin = True
                seg_kind = line.strip('-')
                seg_lines = []
            else:
                seg_begin = False
                segs.append({'kind': seg_kind, 'lines': seg_lines})
            continue


        if seg_begin:
            seg_lines.append(line)

    return segs

def parse_seg1(seg1):
    '''得到文件名 文本转py类型'''
    chart_name = seg1['lines'][0]
    data = [eval(x) for x in seg1['lines'][1:-1]]
    return {'chart': chart_name, 'kind': seg1['kind'], 'data': data}

def assign_peak_to_integral_seg(chart1_integral_shift_dict):
    '''
        chart1_integral_shift_dict 形如 {'integral':XXX, 'shift': YYY}
        输出 [{'integral_range': (left, right), 'integral_area': area, 'shift': []}]
    '''
    integral_segs = chart1_integral_shift_dict['integral']
    shifts_all = chart1_integral_shift_dict['shift']
    res = []
    for integral_area, integral_side1, integral_side2 in integral_segs:
        integral_left = min(integral_side1, integral_side2)
        integral_right = max(integral_side1, integral_side2)
        shifts_in_integral_range = [ shift for shift in shifts_all if integral_left <= shift <= integral_right]
        shifts_in_integral_range = sorted(shifts_in_integral_range, reverse=True)
        res.append({'integral_range':(integral_right, integral_left), #同样先大 后小 20200902 23:23
                    'integral_area': integral_area,
                    'shift': shifts_in_integral_range,
                    })
    return res



def test_format_out_line1():
    #模拟输出
    integral_range = (0, 1)
    area = 1.01
    #shift = 4.03
    peaks = [0.0, 1.0, 2 ,4,5,6,7]
    line1 = format_out_line1(integral_range, area, peaks)
    print(line1)


def my_cli(file_srcv, file_output):
    with open(file_srcv, 'r') as f:
        lines_src = [line.strip('\n') for line in f.readlines()]
    
    #print(lines_src)

    segs = parse_segs(lines_src)
    #print(segs)
    segs = [parse_seg1(seg1) for seg1 in segs]
    #print(segs)
    #get_chart_name
    chart_names = set([seg1['chart'] for seg1 in segs])
    #print(chart_names)
    #得到{'MNovaHtestset/1H.png': {'integral':XXX, 'shift': YYY},...}
    chart_integral_shift_dict = {}
    for chart_name in chart_names:
        segs_chart1 = [seg1 for seg1 in segs if seg1['chart'] == chart_name]
        chart_integral_shift_dict[chart_name] = {k : [seg1 for seg1 in segs_chart1 if seg1['kind'] == k][0]['data'] for k in ['integral', 'shift']}
    #print(chart_integral_shift_dict)

    chart_data_dict = {name: assign_peak_to_integral_seg(data) for name, data in chart_integral_shift_dict.items()}
    print(chart_data_dict)
    #test_format_out_line1()

    chart_separator = '---------'
    with open(file_output, 'w') as f:
        for chart_name, integral_ranges in chart_data_dict.items():
            lines_output = [chart_separator, chart_name, *[str(record1) for record1 in integral_ranges], chart_separator, '']
            [f.write(line + '\n') for line in lines_output]




if __name__ == "__main__":
    #file_srcv = './in/brackets - 副本.txt'
    #file_output = './out/test.txt'
    fire.Fire(my_cli)