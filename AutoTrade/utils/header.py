__all__ = ['get_remaining_calls']

def get_remaining_calls(header):
    # 'Remaining-Req': 'group=order; min=198; sec=7'
    remain = header['Remaining-Req']
    splits = remain.split(';')
    type = splits[0].split('=')[1]
    lim_minute = splits[1].split('=')[1]
    lim_second = splits[2].split('=')[1]
    return {'type': type, 'lim_minute': lim_minute, 'lim_second': lim_second}