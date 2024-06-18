def quick_sort(data,l,r):
    if l<r:
        temp = data[l]
        while(l<r):
            while(l<r and data[r] >= temp):
                r=r-1
            if l<r :
                data[l] = data[r]
                l=l+1
            while l<r and data[l] <= temp:
                l=l+1
            if l<r:
                data[r] = data[l]
                r=r-1
        data[l] = temp
        quick_sort(data,left,l-1)
        quick_sort(data,l+1,right)
    return data

# 默认最大递归深度1000
data = [22,7,11]
left = 0
right = len(data) - 1
print(quick_sort(data,left,right))