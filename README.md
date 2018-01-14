# GoTop
快速使用

1.安装python 3.x。

2.用数据线连接手机和电脑，勾选开发者选项，允许访问数据

找一张题目出现的截图

在main.py的目录下打开命令行界面，输入

      python main.py
	  
3.根据报错，用pip安装相应的包，比如：

	pip install keyboard

	pip install baidu-aip

	pip install terminaltables

注意：需要以管理员身份运行cmd

4.登陆自己的百度账号，在开发者控制台那里，

找到自己的app_id ,app_key，access_key等等，代码里面填的这个是不能用的

5.如果出现识别乱码，比如问题的一部分识别到答案里面去了，那是在截屏时位置不对

因为每个人的手机屏幕不一样，需要改动的地方是

ocr/android.py里面的parse_answer_area()函数

那几个left,right,up,down的意思是，以手机像素为单位截取方框的起始点，相对左上角的位置

屏幕左上角的坐标为（0,0），其他点都相对于这个坐标

已经多次测试，一般不需要改动

6.出现题目的一瞬间，按下enter建。
肯定回答和否定回答的意思，我懒得说了，这都不明白还是别用了