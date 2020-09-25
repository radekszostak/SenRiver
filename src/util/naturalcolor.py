

from functools import reduce
def getNaturalColor(B02, B03, B04):
    def sum(a, b):
        return a + b

    def zip(a, b, f):
        def function(e):
            return f(e[1], b[e[0]])
        return list(map(function, list(enumerate(a))))


    def mapConst(arr, c, f):
        def function(e):
            return f(e[1], c, e[0])
        return list(map(function, list(enumerate(arr))))

    def dotSS(a, b, o=0):
        return a*b


    #vector * scalar
    def dotVS(v, s, o=0):
        return mapConst(v, s, dotSS)


    #vector . vector
    def dotVV(a, b, o=0):
        return reduce(sum,zip(a, b, dotSS))


    #matrix . vector
    def dotMV(A, v, o=0):
        return mapConst(A, v, dotVV)


    def adj(C):
        return (12.92 * C) if C < 0.0031308 else (1.055 * pow(C, 0.41666) - 0.055)


    def labF(t):
        return pow(t,1.0/3.0) if t > 0.00885645 else (0.137931 + 7.787 * t)


    def invLabF(t):
        return  (t*t*t) if t > 0.2069 else (0.12842 * (t - 0.137931))


    def XYZ_to_Lab(XYZ):
        lfY = labF(XYZ[1])
        return [(116.0 * lfY - 16)/100,
            5 * (labF(XYZ[0]) - lfY),
            2 * (lfY - labF(XYZ[2]))]


    def Lab_to_XYZ(Lab):
        YL = (100*Lab[0] + 16)/116
        return [invLabF(YL + Lab[1]/5.0),
                invLabF(YL),
                invLabF(YL - Lab[2]/2.0)]


    def XYZ_to_sRGBlin(xyz):
        return dotMV([[3.240, -1.537, -0.499], [-0.969, 1.876, 0.042], [0.056, -0.204, 1.057]], xyz)


    def XYZ_to_sRGB(xyz):
        return list(map(adj,XYZ_to_sRGBlin(xyz)))


    def Lab_to_sRGB(Lab):
        return XYZ_to_sRGB(Lab_to_XYZ(Lab))


    def getSolarIrr():
        return [B02, 0.939*B03, 0.779*B04]


    def S2_to_XYZ(rad, T, gain):
        return dotVS(dotMV(T, rad), gain)


    def ProperGamma_S2_to_sRGB(rad, T, gg, gamma, gL):
        XYZ = S2_to_XYZ(rad, T, gg)
        Lab = XYZ_to_Lab(XYZ)
        L = pow(gL * Lab[0], gamma)
        return Lab_to_sRGB([L, Lab[1], Lab[2]])


    T = [
    [0.268,0.361,0.371],
    [0.240,0.587,0.174],
    [1.463,-0.427,-0.043]
    ]

    # Gamma and gain parameters
    gain = 2.5
    gammaAdj = 2.2
    gainL = 1

    return ProperGamma_S2_to_sRGB(getSolarIrr(), T, gain, gammaAdj, gainL)
