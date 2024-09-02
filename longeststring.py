from collections import defaultdict

class Solution:
    def longestSubstring(self, s: str, k: int) -> int:
        count = defaultdict(int)
        for c in s:
            count[c] += 1

        temp = defaultdict(list)
        sample = 0
        for c in s:
            if count[c] >= k:
                temp[sample].append(c)
            else:
                sample += 1

        for n in temp.items():
            print(n)
        print(0)


if __name__ == '__main__':
    s = 'abbbccaaaabzabc'
    Solution().longestSubstring(s, 4)