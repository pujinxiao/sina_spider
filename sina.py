# -*- coding:utf-8 -*-
import win32serviceutil
import win32service
import win32event
import re,requests,time,datetime,pymysql,random
WB_count1=8;WB_count=9;w1=0;Stop_py=1;w2=0
get_status=0
class crawl1:
    def __init__(self):
        pass
    def getcontent(self,start_url1):
        '''获取信息'''
        global WB_count1,time_int,picture_name,cont_soure,cont,WB_count
        html=requests.get(start_url1,cookies=cookie,headers=header,timeout=15)
        html=html.content
        reg=r't2\\">粉丝<\\/sp.*?ass=\\"S_line1\\">.*?ong clas.*?">(.*?)<\\/strong><span class=\\"S_txt2\\">微博'
        WB_count=re.findall(re.compile(reg),html)  #发微博数量
        if WB_count==[]:
            self.GetBadCookie(I_D)
            print 'cookie 被冻结'
            cont,picture_name,cont_soure,time_int='1','1','1','1'
            return cont,picture_name,cont_soure,time_int
        else:
            reg1=r'<a name=.*? target=\\"_blank\\" href=\\"\\(.*?)" title=\\"(.*?)\\" date.*?a> 来自 <a'
            WB_url=re.findall(re.compile(reg1),html)[1:2]   #真实数据有15条
            for j in WB_url:
                time_send=j[1]
                timeArray = time.strptime(j[1], "%Y-%m-%d %H:%M")
                time_int=int(time.mktime(timeArray))   #发表时间
                fin_url='http://weibo.com'+j[0].replace('\\','')
                html1=requests.get(fin_url,cookies=cookie,headers=header,timeout=15)
                html1=html1.content
                reg_time=r'<div class=\\"WB_from S_txt2\\">.*?ass=\\"S_txt2\\" target=\\"_blank\\" href=\\"(.*?)" title=\\".*?" date=\\".*?" node-type=\\"feed_list_item_d.*?来自'
                zhuan_url=re.findall(re.compile(reg_time),html1)
                if zhuan_url!=[]:
                    #zhuan_fin_url='http://weibo.com'+zhuan_url[0].replace('\\','')
                    #留着处理转发的微博
                    #logging_a='转发微博'
                    print '转发微博',datetime.datetime.now()
                    #logging.debug(logging_a)
                else:
                    reg3=r'<div class=\\"WB_text W_f14\\" node-type=\\"feed_list_content\\" nick-name=\\"(.*?)\\">(.*?)<!-- 引用文件时'
                    cont=re.findall(re.compile(reg3),html1)[0][1]
                    regg=re.compile(r'<[^>]+>',re.S)
                    cont=regg.sub('',cont).replace('\\n',' ')
                    cont="".join(cont.split())   #正文
                    cont_soure=re.findall(re.compile(reg3),html1)[0][0]  #来源

                    regimg=r'<!-- 引用文件时，必须对midia_info赋值 -->(.*?)<!-- super card-->'
                    img=re.findall(re.compile(regimg),html1)[0]
                    regimg1=r'<img src=\\"(.*?)\\">'
                    img=re.findall(re.compile(regimg1),img)
                    picture_name=[]
                    if img!=[]:
                        for item in img:
                            item_ringht=item.replace('\\','').replace('thumb150','mw690').replace('orj360','mw690')
                            picture=requests.get(item_ringht)
                            name=str('E:\\sina_image\\'+item[-15:])
                            picture_name.append(item[-15:])  #图片名称
                            try:
                                f=open(name,'wb')
                                f.write(picture.content)
                            except Exception,e:
                                print e,'picture'
                            finally:
                                f.close()
                    get_status=1
                    return cont,picture_name,cont_soure,time_int,time_send,get_status
                cont,picture_name,cont_soure,time_int,time_send,get_status=0,0,0,0,0,0
                return cont,picture_name,cont_soure,time_int,time_send,get_status
    def connectDB(self):
        '''链接数据库'''
        host="localhost"
        dbName="sina"
        user="root"
        password="root"
        db=pymysql.connect(host,user,password,dbName,charset='utf8')
        return db
        cursorDB = db.cursor()
        return cursorDB
    def creatTable(self,createTableName):
        '''创建数据库'''
        try:
            createTableSql="CREATE TABLE IF NOT EXISTS "+ createTableName+"(id int(11) NOT NULL AUTO_INCREMENT,content TEXT,photo TEXT,url_name VARCHAR(255),time_in int,PRIMARY KEY (`id`))ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='微博信息'"
            DB_create=self.connectDB()
            cursor_create=DB_create.cursor()
            cursor_create.execute(createTableSql)
        except Exception,e:
            print e,'------creatTable_def'
        finally:
            DB_create.close()
        #logging_b='create_ table '+createTableName+' successfully -------','start spider,now!'
        print 'create_ table '+createTableName+' successfully -------','start spider,now!'
        #logging.debug(logging_b)
        return createTableName
    def SelectUrl(self):
        '''
        读取weibo_id_list中url字段
        把所需要爬取的微博url，添加到start_url（列表）中，供爬取
        '''
        global start_url
        start_url=[]
        selectUrlSql="select url from weibo_id_list"
        DB_select=self.connectDB()
        cursor_select=DB_select.cursor()
        cursor_select.execute(selectUrlSql)
        results = cursor_select.fetchall()
        for i in results:
            start_url.append(i[0])
        DB_select.commit()
        DB_select.close()
    def GetBadCookie(self,ID):
        '''
        记录没用的cookie
        默认valid有用为1，但是被禁就变成0
        '''
        updateContentSql="update cookies_list set valid=0 where id="+str(ID)
        DB_update=self.connectDB()
        cursor_uodate=DB_update.cursor()
        cursor_uodate.execute(updateContentSql)
        DB_update.commit()
        DB_update.close()
    def Selectcookie(self):
        '''
        提取出cookies
        返回：一条cookies'''
        global I_D,Stop_py
        selectContentSql="select id,cookie,valid from cookies_list where valid=1"
        DB_select=self.connectDB()
        cursor_select=DB_select.cursor()
        cursor_select.execute(selectContentSql)
        results = cursor_select.fetchall()
        if results==():
            Stop_py=0   #标记结束py程序
        random_index_ck=random.randint(0,int(len(results)-1))
        I_D = results[random_index_ck][0]
        results = eval(results[random_index_ck][1]) #随机提取cookie
        DB_select.commit()
        DB_select.close()
        return results
    def SelectUA(self):
        '''
        提取出User-Agent
        返回：一个User-Agent
        '''
        selectUA_sql="select header,valid from headers_list where valid=1"
        DB_select=self.connectDB()
        cursor_select=DB_select.cursor()
        cursor_select.execute(selectUA_sql)
        results = cursor_select.fetchall()
        random_index_UA=random.randint(0,int(len(results)-1))
        results = eval(results[random_index_UA][0]) #随机提取header
        DB_select.commit()
        DB_select.close()
        return results
    def inserttable_logging(self,insert1,insert2,insert3,insert4,insert5):
        '''监控数据插入表中'''
        global w2
        insertLoggingSql="insert into weibo_logging"+"(weibo_id,spider_time,get_status,content,time_send)values(%s,%s,%s,%s,%s)"
        DB_insert=self.connectDB()
        cursor_insert=DB_insert.cursor()
        cursor_insert.execute(insertLoggingSql,(str(insert1),str(insert2),str(insert3),str(insert4),str(insert5)))
        w2=w2+1
        print 'logging successfully %s records'%(w2)
        DB_insert.commit()
        DB_insert.close()
    def inserttable(self,insertTable,insert1,insert2,insert3,insert4):
        '''有效数据插入表中'''
        global w1
        try:
            insertContentSql_0="select content from "+insertTable+" where content="+"\'"+insert1+"\'"   #去重复
            insertContentSql="INSERT INTO "+insertTable+"(content,photo,url_name,time_in)VALUES(%s,%s,%s,%s)"
            DB_insert=self.connectDB()
            cursor_insert=DB_insert.cursor()
            a=self.connectDB().cursor().execute(insertContentSql_0)
            if a:
                #logging_c='repetition!'
                print 'repetition!','########',datetime.datetime.now()
                #logging.debug(logging_c)
            else:
                cursor_insert.execute(insertContentSql,(insert1,insert2,insert3,insert4))
                w1=w1+1
                #logging_d='inert contents to '+insertTable+' successfully crawling number '+str(w1)+' ------ '+insert3+' ------'
                print 'inert contents to '+insertTable+' successfully'+' crawling number %s'% (w1),'------'+insert3+'------',datetime.datetime.now()
                #logging.debug(logging_d)
            DB_insert.commit()
        except Exception,e:
            print e,'inserttable_def'
        finally:
            DB_insert.close()

if __name__=='__main__':
    crawl=crawl1()
    table=crawl.creatTable('weibo_result')  #更改表名
    while 1:
        crawl.SelectUrl()
        for start_url1 in start_url:
            try:
                cookie=crawl.Selectcookie()
                header=crawl.SelectUA()
                cont,picture_name,cont_soure,time_int,time_send,get_status=crawl.getcontent(start_url1)
                crawl.inserttable_logging(cont_soure,str(datetime.datetime.now()),get_status,cont,time_send)
                get_status=0
                if cont!=0:
                    crawl.inserttable(table,cont,'@'.join(picture_name),cont_soure,time_int)
                    time.sleep(5)
                else:time.sleep(10)
            except Exception,e:
                a,b,c,d='error',0,'error','error',
                crawl.inserttable_logging(a,str(datetime.datetime.now()),b,c,d)
                print e,'调用函数'
                #logging.debug(e)
                continue
            finally:
                if Stop_py==0:break
        if Stop_py==0:break
        time.sleep(180)