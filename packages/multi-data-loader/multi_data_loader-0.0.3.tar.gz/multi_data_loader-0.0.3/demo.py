from multi_data_loader.data_loader import load_data

loader = load_data(data=["https://airesources.oss-cn-hangzhou.aliyuncs.com/jkl/nj/%E6%96%87%E7%A8%BF1.mp4"],
          type="url")


for res, ret_timestamp, img_size in loader:
    print(res)
loader.release()