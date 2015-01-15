# -*- coding: utf-8 -*-
import pymssql
import _mssql
import decimal
import uuid
import sys
import string
def doexport():
    buf=raw_input('HandNo:')
    #print buf
    if buf<>'q':
            
        if buf=='all':
            BUpdateAll=1
        else:
            BUpdateAll=0
        #handNo='A-YTZ14060001'
        ##handNo='M-H12080001'
        handNo=buf
        conn=pymssql.connect(host="192.168.1.8",user="SA",password="@mhsz19932004801210",database="wPDMnew")
        cou=conn.cursor()
        if BUpdateAll:
            sql='select R.sStructureName,R.sStructure,B.sHLNo from xjwpdmBaseArtInfo B(NOLOCK) inner join xjwpdmbaseStructure R(NOLOCK) on B.sStructureName=R.sStructureName'
        else:
            sql="select R.sStructureName,R.sStructure,B.sHLNo from xjwpdmBaseArtInfo B(NOLOCK) inner join xjwpdmbaseStructure R(NOLOCK) on B.sStructureName=R.sStructureName where sHLNo='"
            sql=sql+handNo+"' and sIsCancel='N'"
        cou.execute(sql)
        for Row in cou.fetchall():
            ##print str(Row)+'len:'+str(len(Row))
            name = Row[0]
            ##print 'name:'+name
            stu = Row[1]
            ##print 'Struct:'+stu
            sNo= Row[2]
            t = stu.split('/')
            print 'split length:'+str(len(t))
        ##  填充重复区块
            sql="select p.nRepeatBeginPosition,p.nRepeatEndPosition,p.nRepeatTimes from xjwpdmbaseStructureRepeat p "
            sql=sql+"inner join xjwpdmbaseStructure R(NOLOCK) on p.sStructureName=R.sStructureName "
            sql=sql+"inner join xjwpdmBaseArtInfo B(NOLOCK)  on B.sStructureName=R.sStructureName "
            sql=sql+"where sHLNo='"+handNo+"'"
            sql=sql+" order by p.nRepeatBeginPosition"
            ##print sql
            ##print 'name:'+name
            cou.execute(sql,(name))
            newsturc = t
            ##前面有插过区块，就保存偏移量。
            PSoffer = 0
            for onePeat in cou.fetchall():
                #把每次重复填充进纹版列表
                nBegin=onePeat[0]
                nEnd  =onePeat[1]
                nRepts=onePeat[2]
                ##产生一次重复块的切片
                TempPeat=t[nBegin-1:nEnd]
                print 'Repeat:begin,end,len,times:'
                print nBegin-1,nEnd,len(TempPeat),nRepts-1
                TempPeat=TempPeat*(nRepts-1)
                
                Buffront= newsturc[0:(nEnd+PSoffer)]
                ##print 'front:'+ str(len(Buffront))
                Bufafter= newsturc[(nEnd+PSoffer):]
                ##print 'after:'+ str(len(Bufafter))
                newsturc=Buffront+TempPeat+Bufafter
                PSoffer=PSoffer+len(TempPeat)
                ##偏移量有问题，应该是PSoffer=PSoffer+len(TempPeat)
                ##print newsturc
                print 'new size:'+str(len(newsturc))
            print '---------------'
            ##print newsturc
            ##print '最后尺寸'+str(len(newsturc))
            f = open(sNo+".dy","w")
            f.close()
            f = open(sNo+".dy","w+")
            inum=len(newsturc)-1
            f.write(str(inum)+'\n')
            ##翻转成样板的从上到下
            newsturc.reverse()
            for row in newsturc:
                if len(row)>0:
                    s=string.ljust(row,22,'0')
                    f.write(str(int(str(s),2))+',128,8,0'+'\n')
                    ##print row+','+str(len(row))
            f.write('0'+'\n')
            f.write('0'+'\n')
            f.write('0'+'\n')
            f.write('0'+'\n')
            f.write('0'+'\n')
            f.flush()
            f.close()
            print u'已导出纹板图文件：'+sNo+u'.dy'
        conn.close() 
        doexport()
        
if __name__=="__main__":
    doexport()
