# class Solution:
#     def subArraySum(self, arr, n, s):
#         end = -1
#         start = 0
#         current_value = 0
#         for i in range(n):
#             end += 1
#             current_value += arr[i]
#
#             while current_value > s and end > start:
#                 current_value -= arr[start]
#                 start += 1
#
#             if current_value == s:
#                 return [start + 1, end + 1]
#
#         return [-1]
#
#
# if __name__ == '__main__':
#     s = Solution().subArraySum(arr=[1,2,3,4], n =4, s=0)
#     print(s)


class Solution:
    def maxSubarraySum(self, arr, N):
        max_sum = arr[0]
        current_sum = arr[0]

        for i in range(1, N):
            current_sum = max(arr[i], current_sum + arr[i])
            max_sum = max(max_sum, current_sum)

        return max_sum

if __name__ == '__main__':
    s = Solution().maxSubarraySum(arr=[1, 2, 3, -2, 5], N=5)
    print(s)