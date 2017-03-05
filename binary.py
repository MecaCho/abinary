import binhex
def format_bin(number_,bw):
    bin_num = bin(number_).replace('0b','')
    if len(bin_num) != bw:
        bin_num = (bw - len(bin_num)) * '0' +bin_num
    return bin_num

print format_bin(1,5)

print bin(2).replace('0b','')
