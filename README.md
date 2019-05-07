## 应用实践简介

本应用实践中，我们根据不同大数据技术把实践内容组织成各个小项目，每个小项目又分成多个步骤。

由此，当我们完成每一个步骤之后，就能初步了解这项技术的特点和应用方式。

当我们完成每一个小项目后，我们基本就已经用大数据技术解决了点击率预测的实际问题。


项目应用实践使用的数据来源于Kaggle的点击率预测比赛。

比赛地址：https://www.kaggle.com/c/avazu-ctr-prediction

## 应用实践数据

数据下载自：https://www.kaggle.com/c/avazu-ctr-prediction/data

字段描述如下：
* id
* click
* hour
* C1 -- anonymized categorical variable
* banner_pos
* site_id
* site_domain
* site_category
* app_id
* app_domain
* app_category
* device_id
* device_ip
* device_model
* device_type
* device_conn_type
* C14-C21 -- anonymized categorical variables

其中，id唯一且每个id对应一次广告展现，click代表了本次广告展现的时候用户是否点击了广告。

hour记录了本次广告的展现时间，格式是YYMMDD，

C1和后面的C14 – C21是数据提供方认为比较重要但不愿意公开含义的字段。