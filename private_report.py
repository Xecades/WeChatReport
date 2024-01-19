import os
import tools 
import argparse
import sys
from tools import load_config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", '-c', type=str, default="./data/config.yaml")
    parser.add_argument('--name', '-n', type=str, required=True, help='联系人的微信昵称，注意不是微信号也不是备注名')
    args = parser.parse_args()
    args = load_config(args)
    return args


if __name__ == "__main__":
    args = parse_args()
    contacts, messages = tools.load_data(args)
    
    friend, fullname = tools.filter_by_name(messages, args.name)
    folder = f"{args.start_date} to {args.end_date} {fullname}"
    remark = friend["Remark"][0]
    n_mess, n_char = tools.calculate_words(friend)
    latest = tools.get_latest_time(friend)
    cnt = tools.plot_wordcloud(friend, os.path.join(args.output_dir, folder, f"wordcloud_both.png"))
    
    me = friend[friend['Sender'] == args.my_wechat_name]
    me = me.reset_index(drop=True)
    cnt_me = tools.plot_wordcloud(me, os.path.join(args.output_dir, folder, f"wordcloud_me.png"))
    
    ta = friend[friend['Sender'] == fullname]
    ta = ta.reset_index(drop=True)
    cnt_ta = tools.plot_wordcloud(ta, os.path.join(args.output_dir, folder, f"wordcloud_ta.png"))
    
    report = open(os.path.join(args.output_dir, folder, "report.txt"), "w")
    original_stdout = sys.stdout
    sys.stdout = report

    print(f"👏 [{args.my_wechat_name}] 和 [{fullname}] ({remark}) 在{args.start_date}到{args.end_date}的微信聊天报告\n")
    print("📊 你们一共发出了{}条消息，{}个字，平均每条消息{}个字".format(n_mess, n_char, round(n_char / n_mess, 3)))
    print("  其中最晚的一条消息是 [{}] 在 [{}] 发出的，内容是 [{}] ".format(
        latest["Sender"], latest["StrTime"], latest["StrContent"]))
    
    print("\n🔥 你们的热词Top5：")
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    for i in range(min(5, len(cnt))):
        print("  {} [{}] 共出现了{}次".format(emojis[i], cnt[i][0], cnt[i][1]))
    
    emojis = tools.top_emoji(friend)
    print("\n🤚 你们的表情包Top5：")
    print("  ", end="")
    for i in range(min(5, len(emojis))):
        print("{}×{}".format(emojis[i][0], emojis[i][1]), end=" ")
        
    print("\n\n🔥 我的热词Top5：")
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    for i in range(min(5, len(cnt_me))):
        print("  {} [{}] 共使用{}次".format(emojis[i], cnt_me[i][0], cnt_me[i][1]))
    
    emojis = tools.top_emoji(me)
    print("\n🤚 我的表情包Top5：")
    print("  ", end="")
    for i in range(min(5, len(emojis))):
        print("{}×{}".format(emojis[i][0], emojis[i][1]), end=" ")
    
    print("\n\n🔥 TA的热词Top5：")
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    for i in range(min(5, len(cnt_ta))):
        print("  {} [{}] 共使用{}次".format(emojis[i], cnt_ta[i][0], cnt_ta[i][1]))
    
    emojis = tools.top_emoji(ta)
    print("\n🤚 TA的表情包Top5：")
    print("  ", end="")
    for i in range(min(5, len(emojis))):
        print("{}×{}".format(emojis[i][0], emojis[i][1]), end=" ")
    
    sys.stdout = original_stdout
    
    tools.plot_nmess_per_minute(friend, os.path.join(args.output_dir, folder, f"nmess_per_minute.png"))  
    tools.plot_nmess_per_month(friend, os.path.join(args.output_dir, folder, f"nmess_per_month.png"))