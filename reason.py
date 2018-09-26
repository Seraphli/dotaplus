class Reasons(object):
    WIN_RATE = 'win_rate'
    ANTI_INDEX_POS = 'anti_index_pos'
    ANTI_INDEX_NEG = 'anti_index_neg'
    ANTI_INDEX = 'anti_index'
    COOP_INDEX_POS = 'coop_index_pos'
    COOP_INDEX_NEG = 'coop_index_neg'
    COOP_INDEX = 'coop_index'
    MATCH_UPS = 'match_ups'
    TEAMMATES = 'teammates'

    N_WIN_RATE = '-win_rate'
    N_ANTI_INDEX_POS = '-anti_index_pos'
    N_ANTI_INDEX_NEG = '-anti_index_neg'
    N_ANTI_INDEX = '-anti_index'
    N_COOP_INDEX_POS = '-coop_index_pos'
    N_COOP_INDEX_NEG = '-coop_index_neg'
    N_COOP_INDEX = '-coop_index'
    N_MATCH_UPS = '-match_ups'
    N_TEAMMATES = '-teammates'


CN_REASON_DICT = {
    Reasons.WIN_RATE: '胜率高',
    Reasons.ANTI_INDEX_POS: '克制系数好',
    Reasons.ANTI_INDEX_NEG: '克制系数好',
    Reasons.ANTI_INDEX: '克制系数好',
    Reasons.COOP_INDEX_POS: '队友系数好',
    Reasons.COOP_INDEX_NEG: '队友系数好',
    Reasons.COOP_INDEX: '队友系数好',
    Reasons.MATCH_UPS: '克制',
    Reasons.TEAMMATES: '配合',

    Reasons.N_WIN_RATE: '胜率低',
    Reasons.N_ANTI_INDEX_POS: '克制系数差',
    Reasons.N_ANTI_INDEX_NEG: '克制系数差',
    Reasons.N_ANTI_INDEX: '克制系数差',
    Reasons.N_COOP_INDEX_POS: '队友系数差',
    Reasons.N_COOP_INDEX_NEG: '队友系数差',
    Reasons.N_COOP_INDEX: '队友系数差',
    Reasons.N_MATCH_UPS: '被克制',
    Reasons.N_TEAMMATES: '不配合',
}


def get_good_reason_cn(hero, reasons, data):
    _reason = []
    for r in CN_REASON_DICT:
        if '-' not in r and hero in reasons[r]:
            if r == Reasons.MATCH_UPS or r == Reasons.TEAMMATES:
                _reason.append(CN_REASON_DICT[r] + ':' +
                               ','.join([data[h]['cn_name']
                                         for h in reasons[r][hero]]))
            elif CN_REASON_DICT[r] not in _reason:
                _reason.append(CN_REASON_DICT[r])

    return ';'.join(_reason)


def get_bad_reason_cn(hero, reasons, data):
    _reason = []
    for r in CN_REASON_DICT:
        if '-' in r and hero in reasons[r]:
            if r == Reasons.N_MATCH_UPS or r == Reasons.N_TEAMMATES:
                _reason.append(CN_REASON_DICT[r] + ':' +
                               ','.join([data[h]['cn_name']
                                         for h in reasons[r][hero]]))
            elif CN_REASON_DICT[r] not in _reason:
                _reason.append(CN_REASON_DICT[r])

    return ';'.join(_reason)
