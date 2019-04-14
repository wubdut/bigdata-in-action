1. $hdfs -dfs -ls /

2. $sudo -u hdfs hdfs -mkdir /exp
   $sudo -u hdfs hdfs -chmod 777 /exp

3. $hdfs -dfs -touchz /exp/file

4. $sudo -u hdfs hdfs -dfs -rm /exp/file

5. $sudo -u hdfs hdfs -dfs -rm r /exp