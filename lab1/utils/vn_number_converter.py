class VNNumConverter:
    def __init__(self):
        self.number_to_string = {
            0: "không",
            1: "một",
            2: "hai",
            3: "ba",
            4: "bốn",
            5: "năm",
            6: "sáu",
            7: "bảy",
            8: "tám",
            9: "chín",
        }
        self.num_excep_to_string = {
            0: "",
            1: "mốt",
            2: "hai",
            3: "ba",
            4: "bốn",
            5: "lăm",
            6: "sáu",
            7: "bảy",
            8: "tám",
            9: "chín",
        }
        self.digits = ["tỷ", "triệu", "nghìn", "."]

    def get_length(self, num):
        string = str(num)
        count = len(string)
        return count

    def ones(self, num):
        result = []
        result.append(self.number_to_string[num])
        return result

    def dezons(self, num):
        result = []
        if num // 10 != 1:
            result += self.ones(num // 10)
            result.append("mươi")
            if num % 10 == 0:
                return result
            else:
                result.append(self.num_excep_to_string[num % 10])
        else:
            result.append("mười")
            if num % 10 == 1:
                result.append("một")
            else:
                if num % 10 == 0:
                    return result
                else:
                    result.append(self.num_excep_to_string[num % 10])
        return result

    def hunreds(self, num):
        result = []
        result.append(self.number_to_string[num // 100])
        result.append("trăm")

        if (num % 100) // 10 != 0:
            result += self.dezons(num % 100)
        else:
            if (num % 100) % 10 == 0:
                return result
            else:
                result.append("lẻ")
                result += self.ones(num % 10)
        return result

    def read_number(self, count, num):
        if count == 1:
            return self.ones(num)
        elif count == 2:
            return self.dezons(num)
        elif count == 3:
            return self.hunreds(num)
        else:
            raise TypeError

    def number_to_vntext(self, num):
        if num == 0:
            return self.ones(num)

        divisor = 10**9
        result = []
        i = 0
        while num != 0:
            if num // divisor != 0:
                count = self.get_length(num // divisor)
                if len(result) != 0:
                    if count == 2:
                        result.append("không")
                        result.append("trăm")
                    if count == 1:
                        result.append("không")
                        result.append("trăm")
                        result.append("linh")
                result += self.read_number(count, num // divisor)
                result.append(self.digits[i])
                num %= divisor
                divisor //= 1000
                i += 1
            else:
                i += 1
                divisor //= 1000

        if result[len(result) - 1] == ".":
            del result[len(result) - 1]

        return result