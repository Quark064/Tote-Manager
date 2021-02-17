testing = "01008551950064491724103110OR00977"
testchp = "00855195006449"
heyther = "R S H H M D"
print(testing[18:24])

class decodeBarcode:
    def __init__(self, bcStr):
        self.expDate = "20{}-{}-{}".format(bcStr[18:20], bcStr[20:22], bcStr[22:24])
        self.lot = bcStr[26:]
        self.ref = bcStr[2:16]

hey = decodeBarcode(testing)
print(hey.ref)
print(hey.lot)
print(hey.expDate)
