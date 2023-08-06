from django.shortcuts import render  # type: ignore

# from blogs.models import Category, Blog
from django_pandas.io import read_frame  # type: ignore

from .models import GoogleAccess

# from matplotlib.backends.backend_agg import FigureCanvasAgg

# import io
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import seaborn as sns
# sns.set_style('darkgrid')
# import numpy as np
# import japanize_matplotlib


def index(request):
    """
    Dataアプリトップページ
    グラフ表用にpandasを使用してテーブルの処理

    """
    qs = GoogleAccess.objects.all()

    # データをテーブル形式に変換
    df = read_frame(qs, fieldnames=["date_data", "access_data"])

    # アクセス数の合計
    access_sum = "{:,}".format(df["access_data"].sum())

    # 日付を再設定
    df["date_data"] = df["date_data"].apply(lambda df: df.strftime("%Y年%m月"))

    # 日付を元にアクセス数を集約する
    df = df["access_data"].groupby(df["date_data"]).sum().reset_index()

    # アクセス数を１段ずらしてカラムを作成
    # df = df.join(df['access_data'].shift(1).rename('previous_month'))

    # アクセス数を１２段ずらしてカラムを作成
    # df = df.join(df['access_data'].shift(12).rename('past_months'))

    # 底から１２段を変数に格納
    df = df.tail(12)

    # データタイプを整数型に変更
    # df['past_months'] = df['past_months'].astype(int)

    # 前年月との差分を出しカラムを作成
    # df['months_error'] = df['access_data'] - df['past_months']

    # 先月との差分を出しカラムを作成
    # df['previous_month_error'] = df['access_data'] - df['previous_month']

    # データタイプを整数型に変更
    # df['previous_month_error'] = df['previous_month_error'].astype(int)
    context = {"df": df, "access_sum": access_sum}
    return render(request, "data/index.html", context)


# def blogs_plot(request):
#     """
#     Blogカテゴリーのグラフ
#
#     """
#     plt.rcParams.update({'figure.autolayout': True})
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     fig.patch.set_facecolor('whitesmoke')#背景の指定
#
#     """ここにデータを作成する"""
#     category_choice = Category.objects.all()
#     blogs_choice = Blog.objects.select_related('category').all()
#
#     x1 = [data.title for data in category_choice]
#     y1 = [data.category_id for data in blogs_choice]
#     y1 = np.unique(y1, return_counts=True)
#
#     colorlist = ['r', 'y', 'g', 'b', 'm', 'c', '#ffff33', '#f781bf']
#     ax.bar(x1, y1[1], color=colorlist, width=0.3, alpha=0.5)
#
#     buf = io.BytesIO()
#     canvas = FigureCanvasAgg(fig)
#     canvas.print_png(buf)
#     response = HttpResponse(buf.getvalue(), content_type='image/png')
#     fig.clear()
#     response['Content-Length'] = str(len(response.content))
#     return response
