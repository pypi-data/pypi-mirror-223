from django.db import models # type: ignore


class GoogleAccess(models.Model):
    """
    GoogleAnalyticsのアクセス情報保存

    """
    date_data = models.DateField('年月')
    access_data = models.IntegerField('アクセス数')

    def __str__(self):
        return str(self.date_data)

    class Meta:
        verbose_name = 'グーグルアクセスデータリスト'
        verbose_name_plural = 'グーグルアクセスデータリスト'


class Popular(models.Model):
    """
    GoogleAnalytics APIモデル
    blogsアプリで使用しているので、後にblogsアプリに移行

    """
    title = models.CharField('人気記事', max_length=100)
    path = models.CharField('URL', max_length=100)
    view = models.IntegerField('閲覧数')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '人気記事リスト'
        verbose_name_plural = '人気記事リスト'
