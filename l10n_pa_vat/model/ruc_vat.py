#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Reference:
# https://www.anip.gob.pa/documentos/DV_RUC.pdf

_arrval = {
        '00': '00',
        '10': '01',
        '11': '02',
        '12': '03',
        '13': '04',
        '14': '05',
        '15': '06',
        '16': '07',
        '17': '08',
        '18': '09',
        '19': '01',
        '20': '02',
        '21': '03',
        '22': '04',
        '23': '07',
        '24': '08',
        '25': '09',
        '26': '02',
        '27': '03',
        '28': '04',
        '29': '05',
        '30': '06',
        '31': '07',
        '32': '08',
        '33': '09',
        '34': '01',
        '35': '02',
        '36': '03',
        '37': '04',
        '38': '05',
        '39': '06',
        '40': '07',
        '41': '08',
        '42': '09',
        '43': '01',
        '44': '02',
        '45': '03',
        '46': '04',
        '47': '05',
        '48': '06',
        '49': '07'
        }

def _digitDV(sw, ructb):
    # rutina calcula dv
    j = 2
    nsuma = 0

    for c in reversed(ructb):
        if sw and j == 12:
            sw = False
            j -= 1

        nsuma += j*(ord(c)-ord('0'))
        j += 1
    r = nsuma % 11
    if r > 1:  return 11 - r
    return 0

def calculateDV(ruc):
    rs = ruc.split('-')
    #print "cedula o ruc",rs
    #print "lenght_rs",len(rs)
    # Not right, PI, AV, SB, NT all have 4 fields
    #if (len(rs) == 4 and rs[1] != 'NT') or len(rs) < 3 or len(rs) > 5:
    if len(rs) < 3 or len(rs) > 5:
    #if (len(rs) == 4 and rs[1] != 'NT') or (len(rs) == 4 and rs[1] != 'PI') or (len(rs) == 4 and rs[1] != 'AV') or (len(rs) == 4 and rs[1] != 'SB') or len(rs) < 3 or len(rs) > 5:
        return ''

    sw = False

    # TODO: NT y SB
        # Los E estan OK, 23 posiciones
    if ruc[0] == 'E':
        ructb = '0'*(2-len(rs[1])) + '0000005' + '00' + '50' + '0'*(3-len(rs[1])) + rs[1] + '0'*(5-len(rs[2])) + rs[2]
        #print "Tipo E"
        #print "caracteres",len(ructb)
        # 4 campos
    elif rs[0][:-1] == 'N' and rs[1] == 'NT':
        ructb = '0'*(3-len(rs[0])) + '0000005' + '0'*(1-len(rs[0][:-2])) + rs[0][1:] + rs[1][:-2] + '43' + '0'*(3-len(rs[2])) + rs[2] + '0'*(5-len(rs[3])) + rs[3]
        #print "Tipo NT Natural"
        #print ructb
        #print "caracteres",len(ructb)
        # 4 campos
    elif rs[1] == 'NT':
        ructb = '0'*(2-len(rs[0])) + '0000000' + '0'*(2-len(rs[0])) + rs[0] + rs[1][:-2] + '43' + '0'*(3-len(rs[2])) + rs[2] + '0'*(5-len(rs[3])) + rs[3]
        #print "Tipo NT Juridico"
        #print ructb
        #print "caracteres",len(ructb)
        # 4 campos
    elif rs[1] == 'AV':
        ructb = '0'*(2-len(rs[0])) + '0000005' + '0'*(2-len(rs[0])) + rs[0] + rs[0][:-2] + '15' + '0'*(3-len(rs[2])) + rs[2] + '0'*(5-len(rs[3])) + rs[3]
        #print "Tipo AV"
        #print "caracteres",len(ructb)
        # 4 campos
    elif rs[1] == 'PI':
        ructb = '0'*(2-len(rs[0])) + '0000005' + '0'*(2-len(rs[0])) + rs[0] + rs[1][:-2] + '79' + '0'*(3-len(rs[2])) + rs[2] + '0'*(5-len(rs[3])) + rs[3]
        #print "Tipo PI"
        #print "caracteres",len(ructb)
        # Los PE estan OK, 21 posiciones
    elif rs[0] == 'PE':
        if len(rs[1]) > 3:
            cutrs1 = rs[1][1:]
            #print "cutrs1", cutrs1
            ructb = '0'*(5-len(rs[1])) + '0000005' + '0' + '74' + '0'*(4-len(rs[1])) + rs[1] + '0'*(5-len(rs[2])) + rs[2]
        elif len(rs[1]) <=3:
            ructb = '0'*(3-len(rs[1])) + '0000005' + '00' + '75' + '0'*(3-len(rs[1])) + rs[1] + '0'*(5-len(rs[2])) + rs[2]
        #print "Tipo PE"
        #print rs
        #print "00000005007500100019"
        #print ructb
        #print "caracteres",len(ructb)
        # Los N estan OK, 21 positiones
    elif ruc[0] == 'N':
        ructb = '0'*(3-len(rs[1])) + '0000005' + '00' + '40' + '0'*(3-len(rs[1])) + rs[1] + '0'*(5-len(rs[2])) + rs[2]
        #print "Tipo N"
        #print ructb
        #print "caracteres",len(ructb)
        # 4 campos
        # Son las cedulas normales, esta OK, 20 positiones?
#    elif 0 < len(rs[0]) <= 2:
    elif len(rs[0]) == 1 or rs[0] == '10' or rs[0] == '11' or rs[0] == '12' or rs[0] == '13':
        ructb = '0'*(4-len(rs[1])) + '0000005' + '0'*(2-len(rs[0])) + rs[0] + '00' + '0'*(3-len(rs[1])) + rs[1] + '0'*(5-len(rs[2])) + rs[2]
        #print "Persona Natural"
        #print ructb
        #print "caracteres",len(ructb)
    else: # RUC juridico, 20 positiones, OK
        ructb = '0'*(10-len(rs[0])) + rs[0] + '0'*(4-len(rs[1])) + rs[1] + '0'*(6-len(rs[2])) + rs[2]
        #print "Tipo Juridico"
        #print rs[0]
        #print "caracteres",len(ructb)
        #print ructb

        # sw es true si es ruc antiguo
        sw = ructb[3] == '0' and ructb[4] == '0' and ructb[5] < '5'

    # rutina de referencia cruzada
    if sw:
        ructb = ructb[:5] + _arrval.get(ructb[5:7],ructb[5:7]) + ructb[7:]

    #if sw == 'True':
        #print "Antiguo =", sw
    #print ructb

    dv1 = _digitDV(sw, ructb)
    #print "DV1",dv1
    dv2 = _digitDV(sw, ructb+chr(48+dv1))
    #print "Resultado DV =",dv1,dv2

    ret =  chr(48+dv1) + chr(48+dv2)
    #print ret
    return ret

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='DV calculator')
    parser.add_argument('ruc', type=str)
    args = parser.parse_args()

    dv = calculateDV(args.ruc)
    if len(dv) == 0:
        sys.exit(1)
    #print "DV =",dv
