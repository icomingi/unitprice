#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unittest

GRAM = re.compile(r"(([0-9]+\.?\d{0,3})(g|kg|克|千克|斤|升|毫升|l|ml)(\*([0-9]+))?)", re.IGNORECASE)

NET = re.compile(r"(([0-9]+\.?\d{0,3})(g|mg|kg|克|千克|斤|升|毫升|l|ml)(\s*[\*x]\s*([0-9]+))?)", re.IGNORECASE)

GRAM_BONUS = re.compile(r"([0-9]+\.?\d{0,2}(g|kg|克|千克|斤))\+([0-9]+\.?\d{0,2}(g|kg|克|千克|斤))", re.IGNORECASE)
LITRE = re.compile(r"([0-9]+\.?\d{0,2}(ml|l|毫升|升)(\*([0-9]+))?)", re.IGNORECASE)

CONVERSION_TABLE = (('g', 'g', 1),
                    ('mg', 'g', 0.001),
                    ('kg', 'g', 1000),
                    ('克', 'g', 1),
                    ('千克', 'g', 1000),
                    ('斤', 'g', 500),
                    ('升', 'ml', 500),
                    ('毫升', 'ml', 1),
                    ('ml', 'ml', 1),
                    ('l', 'ml', 1000)
                   )


class KnownValues(unittest.TestCase):
    knownValues = (("含量100g", "100.0g"),
                   ("254g", "254.0g"),
                   ("254.12kg", "254120.0g"),
                   ("contains1000kgstuff", "1000000.0g"),
                   (u"200克", "200.0g"),
                   ("五谷杂粮3千克", "3000.0g"),
                   ("黄飞红甜麻辣花生脆188g*5", "940.0g"),
                   ("乐事美国经典原味75g", "75.0g"),
                   ("优滋果黄桃e果杯整箱装235g*24杯", "5640.0g"),
                   ("甜甜乐星球杯大桶装（巧克力味酱+饼干粒）950G", "950.0g"),
                   ("京东美客多糖水梨球水果罐头提手礼盒220g*12瓶【双诞大驾光临 大牌利器再现】 绝", "2640.0g"),
                   ("北大荒有机十二种杂粮礼盒 4.8KG (真空包装)“每”满200-20，北大荒元旦钜惠，新粮", "4800.0g"),
                   ("十月稻田五常稻花香大米 25kg2013年新米上市！东北大米 香米 五常大米 稻花香大米 ", "25000.0g"),
                   ("绿之源农庄有机大米2.5kg", "2500.0g"),
                   ("香港金像牌面包粉1千克/袋 高筋面粉中国大陆销售的唯一正品 中文包装 顶级高筋面", "1000.0g"),
                   ("香港金像牌面包粉1千克*5袋 高筋面粉【支持货到付款】中国大陆销售的唯一正品 顶", "5000.0g"),
                   ("金桔5.2斤", "2600.0g"),
                   ("绿力 番石榴汁饮料 490ml（台湾地区） 来自台湾地区的经典美味 高端洋气", "490.0ml"),
                   ("Cyprina塞浦丽娜 橙汁 C.A.E 1L 塞浦路斯进口 进口食品 果汁/纯果蔬汁 营", "1000.0ml"),
                   ("五谷杂粮 天地粮人一等精选有机东北红小豆 加量促销装1200g+150g（自封口包装", "1350.0g"),
                   ("金桔2.4斤+3.6kg", "4800.0g"),
                   )
        
    def testKnownValues(self):
        for raw_string, correct_value in self.knownValues:
#            self.assertEqual(extract_gram(raw_string), correct_value)
#             self.assertEqual(extract_data(raw_string), (float(correct_value[:-1]), correct_value[-1]))
             self.assertEqual(to_str(extract_data(raw_string)), correct_value)

class KnownLitreValues(unittest.TestCase):
    knownValues = (("绿力 番石榴汁饮料 490ml（台湾地区） 来自台湾地区的经典美味 高端洋气", "490ml"),
                   ("Cyprina塞浦丽娜 橙汁 C.A.E 1L 塞浦路斯进口 进口食品 果汁/纯果蔬汁 营", "1000ml"),
    )

#    def testKnownValues(self):
#        for raw_string, correct_value in self.knownValues:
#            self.assertEqual(extract_litre(raw_string), correct_value)
            
def extract_gram(raw_string):
    bonus = GRAM_BONUS.search(raw_string)
    if bonus:
        print bonus.groups()
        raw_string = [bonus.groups()[0], bonus.groups()[2]]
    else:
        raw_string = [raw_string]
    match = map(GRAM.search, raw_string)
    if match:
        for m in match:
            print m.groups()
        result = [all2g(m.groups()) for m in match if m]
#        result = all2g(match.groups())
        print result
        #s = str(int(result[1])) + result[2]
        q = reduce(lambda x, y: x+y, [int(r[1]) for r in result if r])
        return str(q)+"g"

def extract_litre(raw_string):
    pass

def all2g(match):
    quantity = match[4] and int(match[4]) or 1
    unit = match[2].lower()
    if unit == "kg":
        return (match[0], float(match[1])*1000*quantity, 'g', quantity)
    elif unit == "克":
        return (match[0], float(match[1])*quantity, 'g', quantity)
    elif unit == "千克":
        return (match[0], float(match[1])*1000*quantity, 'g', quantity)
    elif unit == "斤":
        return (match[0], float(match[1])*500*quantity, 'g', quantity)
    else:
        return (match[0], float(match[1])*quantity, 'g', quantity)


def extract_data(raw_string):
    match = NET.search(raw_string)
    if match:
        complete, net, unit, star, quantity = match.groups() 
        return standardize(net, unit, quantity)
    else:
        return ('', '')


def standardize(net, unit, quantity):
    net = float(net)
    unit = unit.lower()
    quantity = quantity and int(quantity) or 1
    for unit_from, unit_to, conversion in CONVERSION_TABLE:
        if unit_from == unit:
            return (net*conversion*quantity, unit_to)

def to_str(t):
    return reduce(lambda x, y: str(x) + str(y), t)
    
    
if __name__ == "__main__":
    unittest.main()
