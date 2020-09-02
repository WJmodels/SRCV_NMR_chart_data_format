'''
修改SRCV输出谱图数据格式
'''
#import os

def format_chart1(integral_range, shift, peaks):
	peaks_str = ','.join([str(x) for x in peaks])
	return f'{{integral: ({integral_range[0]}, {integral_range[1]}), shift: {shift}, peak: [{peaks_str}]}}'

if __name__ == "__main__":
    with open('./in/brackets - 副本.txt', 'r') as f:
        lines_src = f.readlines()
    
    #print(lines_src)
    integral_range = (0, 1)
    shift = 4.03
    peaks = [0.0, 1.0, 2 ,4,5,6,7]
    line1 = format_chart1(integral_range, shift, peaks)
    print(line1)