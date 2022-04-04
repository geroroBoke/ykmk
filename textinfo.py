# filename
def get_text_info(text):

    # 小説家になろう
    if "小説家になろうタテ書き小説ネット小説を読もう！" in text:

        # start_navi
        s_start_navi = text.find("<< 前へ次へ >>")
        if s_start_navi < 0 :
            s_start_navi = text.find("<< 前へ")
        if s_start_navi < 0 :
            s_start_navi = text.find("次へ >>")

        # end_navi
        s_end_navi = text.find("<< 前へ次へ >>目次")
        if s_end_navi < 0 :
            s_end_navi = text.find("次へ >>目次")
        elif s_end_navi < 0 :
            s_end_navi = text.find("<< 前へ目次")

        # login
        s_login = text.find("ブックマーク登録する場合はログインしてください。")

        # title
        s_title = text.find("\r\n", s_login) + len("\r\n")
        e_title = text.find("作者：", s_title)

        # author
        s_author = text.find("作者：", s_title)
        e_author = text.find("\r\n", s_author)

        # chapter
        s_chapter = text.find("\r\n", s_author) + len("\r\n")
        e_chapter = text.find("\r\n", s_chapter)
        if s_chapter == s_start_navi:
            e_chapter = s_chapter

        # number
        s_number = text.find("\r\n\r\n", s_start_navi) + len("\r\n\r\n")
        e_number = text.find("\r\n", s_number)

        # episode
        s_episode = text.find("\r\n", s_number) + len("\r\n")
        e_episode = text.find("\r\n", s_episode)

        # content
        s_content = text.find("\r\n", s_episode)
        e_content = s_end_navi

        # print("s_title:{0}".format(s_title))
        # print("s_start_navi:{0}".format(s_start_navi))
        # print("s_end_navi:{0}".format(s_end_navi))
        # print("s_number:{0}".format(s_number))
        # print("s_episode:{0}".format(s_episode))
        # print("s_content:{0}".format(s_content))

        return {
                "title" : text[s_title:e_title],
                "author" : text[s_author:e_author],
                "chapter" : text[s_chapter:e_chapter],
                "number" : text[s_number:e_number],
                "episode" : text[s_episode:e_episode],
                "content" : text[s_content:e_content],
                }
    # ハーメルン
    elif "ホーム 利用規約 FAQ 運営情報 取扱説明書 プライバシーポリシー 情報提供 機能提案 自作フォント ログアウト 夜間モード：" in text:

        # start_navi
        s_start_navi = text.find("×\r\n目 次\r\n次の話 >>")
        e_start_navi = s_start_navi + len("×\r\n目 次\r\n次の話 >>")

        if s_start_navi < 0 :
            s_start_navi = text.find("<< 前の話\r\n目 次\r\n次の話 >>")
            e_start_navi = s_start_navi + len("<< 前の話\r\n目 次\r\n次の話 >>")
        if s_start_navi < 0 :
            s_start_navi = text.find("<< 前の話\r\n目 次\r\n×")
            e_start_navi = s_start_navi + len("<< 前の話\r\n目 次\r\n×")

        # end_navi
        s_end_navi = text.find("×\r\n目 次\r\n次の話 >>", s_start_navi+1)
        if s_end_navi < 0 :
            s_end_navi = text.find("<< 前の話\r\n目 次\r\n次の話 >>", s_start_navi+1)
        if s_end_navi < 0 :
            s_end_navi = text.find("<< 前の話\r\n目 次\r\n×", s_start_navi+1)

        # login
        s_login = text.find("目次 小説情報 一括 縦書き しおりを挟む お気に入り登録 評価 感想 推薦 誤字 ゆかり 閲覧設定 固定")
        if s_login < 0:
            s_login = text.find("目次 小説情報 一括 縦書き しおりを挟む お気に入り登録 評価 感想 推薦 誤字 閲覧設定 固定")
        if s_login < 0:
            s_login = text.find("閲覧設定 固定")

        # title
        s_title = text.find("\r\n", s_login) + len("\r\n")
        e_title = text.find(" 　 作：", s_title)

        # author
        s_author = text.find("作：", s_title)
        e_author = text.find("\r\n", s_author)

        # number
        s_number = text.find("\r\n", e_start_navi) + len("\r\n")
        e_number = text.find("\r\n", s_number)

        # chapter
        s_chapter = text.find("\r\n", s_number) + len("\r\n")
        e_chapter = text.find("\r\n", s_chapter)

        # episode
        s_episode = text.find("\r\n", s_number) + len("\r\n")
        e_episode = text.find("\r\n\r\n", s_episode)
        if e_episode == e_chapter :
            e_chapter = s_chapter
        else:
            s_episode = text.find("\r\n", s_chapter) + len("\r\n")

        # content
        s_content = text.find("\r\n\r\n", s_episode) + len("\r\n\r\n")
        e_content = s_end_navi

        return {
                "title" : text[s_title:e_title],
                "author" : text[s_author:e_author],
                "chapter" : text[s_chapter:e_chapter],
                "number" : text[s_number:e_number],
                "episode" : text[s_episode:e_episode],
                "content" : text[s_content:e_content],
                }
    else:
        return false