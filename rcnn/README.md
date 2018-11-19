##这是利用关键点数据预测的，所以一共五类:衬衫，外套，短裙，长裙，裤子
##所以我训练了6个模型，分布对应衬衫，外套，短裙，长裙，裤子，还有一个是五种一起预测了（效果较差）
##获取框：
```
demo.py --csv data/round2_fashionAI_key_points_test_a_20180426/test.csv --prefix model/ --epoch 0 --vis
```
###如果想用于属性识别，请将文件夹与五类手动对应，可以自行尝试，我这里给出一个参考：
```
prefix = {'lapel_design_labels':'outwear','coat_length_labels':'outwear','collar_design_labels':'blouse',
          'neck_design_labels':'blouse','neckline_design_labels':'dress','skirt_length_labels':'skirt',
          'sleeve_length_labels':'outwear','pant_length_labels':'trousers','skirt':'skirt',
          'blouse':'blouse','outwear':'outwear','trousers':'trousers','dress':'dress'}

```
也可以用多个模型求框，取最大的框框
```
#假设用三个预测了3个框
bbox = np.random.random((3,4)) #3个框，四个坐标（xmin,ymin,xmax,ymax）
xmin = np.min(bbox[:,0])
xmax = np.max(bbox[:,1])
...
```

# 老哥们加油
