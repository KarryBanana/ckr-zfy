from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
import pymysql
from django.http import JsonResponse
import django


def save_doc(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    msg=request.POST['msg']
    userid=request.POST['userid']
    sql="update Table_file set doctext='"+msg+"' where id="+str(id)
    cur.execute(sql)
    sql="update Table_file set lastauthor_id="+str(userid)+",lasttime=now() where id="+str(id)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def change_info(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    msg=request.POST['msg']
    op=request.POST['op']
    op=int(op)
    opc=""
    if op==1:opc="docname"
    elif op==2:opc="doctitle"
    elif op==3:opc="docintro"
    sql="update Table_file set "+opc+"='"+msg+"' where id="+str(id)
    print(sql)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def get_doc(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    op=request.POST['op']
    opc=""
    op=int(op)
    print(op)
    if op==1:opc="doctitle"
    elif op==2:opc="docintro"
    elif op==3:opc="doctext"
    elif op==4:opc="docname"
    sql="select "+opc+" from Table_file where id="+str(id)
    print(sql)
    cur.execute(sql)
    chars=""
    for row in cur:
        chars=row[0]
    con.close()
    return JsonResponse(chars,safe=False)


# def submit_comment(request):
#     con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
#     cur=con.cursor()
#     id=request.POST['id']
#     docnum=request.POST['docnum']
#     content=request.POST['content']
#     sql="insert into Commentlist values('"+content+"',"+str(id)+","+str(docnum)+",now())"
#     cur.execute(sql)
#     sql="select username from auth_user where id="+str(id)
#     cur.execute(sql)
#     for row in cur:
#         username=row[0]
#     sql = "select docname from Table_file where id=" + str(docnum)
#     cur.execute(sql)
#     for row in cur:
#         docname = row[0]
#     content=username+" 评论了您的文档: "+docname+" ,去看看吧!"
#     sql = "select author_id from Table_file where id=" + str(docnum)
#     cur.execute(sql)
#     for row in cur:
#         author_id = row[0]
#     sql = "insert into Noticelist values(," + str(author_id) + ",'" + content + "',now(),0)"
#
#     cur.connection.commit()
#     con.close()
#     return JsonResponse(1,safe=False)
#
#
# def get_comments(request):
#     con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
#     cur=con.cursor()
#     docnum=request.POST['docnum']
#     sql="select auth_user.username,commenttime,content from (auth_user join Commentlist on auth_user.id=Commentlist.id) where docnum="+str(docnum)
#     cur.execute(sql)
#     con.close()
#     return JsonResponse(cur.fetchall(),safe=False)


def submit_comment(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    cid = request.POST['cid']
    uid=request.POST['uid']
    f_cid = request.POST['f_cid']
    f_uid = request.POST['f_uid']
    f_name = request.POST['f_name']
    docnum=request.POST['docnum']
    content=request.POST['content']
    commenttime = request.POST['commenttime']
    sql="insert into Commentlist values('"+content+"',"+str(docnum)+",'"+ commenttime +"',"+str(cid)+","+str(uid)+","+str(f_cid)+","+str(f_uid)+",'"+f_name+"')"
    cur.execute(sql)

    sql = "select username from auth_user where id=" + str(uid)
    cur.execute(sql)
    for row in cur:
        username=row[0]
    sql = "select docname from Table_file where id=" + str(docnum)
    cur.execute(sql)
    for row in cur:
        docname = row[0]
    content=username+" 评论了您的文档: "+docname+" ,去看看吧!"
    sql = "select author_id from Table_file where id=" + str(docnum)
    cur.execute(sql)
    for row in cur:
        author_id = row[0]

    sql="select count(*) from Noticelist"
    cur.execute(sql)
    for row in cur:
        nid=row[0]+1

    sql ="insert into Noticelist values("+str(nid)+","+str(author_id)+",'"+content+"',now(),0,1)"
    cur.execute(sql)
    cur.connection.commit()
    ###
    f_uid=int(f_uid)
    if f_uid!=0:
        content=username+"回复了您在文档 "+docname+" 中的评论,去看看吧!"
        sql = "select count(*) from Noticelist"
        cur.execute(sql)
        for row in cur:
            nid = row[0] + 1
        sql = "insert into Noticelist values(" + str(nid) + "," + str(f_uid) + ",'" + content + "',now(),0,1)"
        cur.execute(sql)
        cur.connection.commit()

    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def get_comments(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    docnum=request.POST['docnum']
    sql="select cid,uid,auth_user.username,content,commenttime,f_cid,f_name from (auth_user join Commentlist on auth_user.id=Commentlist.uid) where docnum="+str(docnum)
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(),safe=False)


def search_docs(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    key=request.POST['key']
    sql="select id,docname,author_id,lasttime from Table_file where (stat=0 or stat=1) and docname like '%"+key+"%'"
    # print(sql)
    cur.execute(sql)
    docs=cur.fetchall()
    rarr = []
    for doc in docs:
        con.ping()
        tmp = {}
        tmp['docnum'] = doc[0]
        tmp['docname'] = doc[1]
        tmp['author'] = doc[2]
        tmp['lasttime'] = doc[3]
        rarr.append(tmp)
    con.close()
    return JsonResponse(rarr,safe=False)


def get_group_docs(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    groupnum=request.POST['groupnum']
    sql="select id,docname,author_id,lasttime from Table_file where stat>-2 and groupnum="+str(groupnum)
    cur.execute(sql)
    con.close()
    docs=cur.fetchall()
    rarr=[]
    for doc in docs:
        con.ping()
        tmp={}
        # print(doc[0])
        # sql="select count(*) from Table_collectlist"
        sql="select count(*) from Table_collectlist where user_id="+str(id)+" and file_id="+str(doc[0])
        print(sql)
        cur.execute(sql)
        isCollected=False
        for row in cur:
            if row[0]>=1:isCollected=True
            else:isCollected=False
        tmp['isCollected']=isCollected
        tmp['docnum']=doc[0]
        tmp['docname']=doc[1]
        tmp['author']=doc[2]
        tmp['lasttime']=doc[3]
        rarr.append(tmp)
    print(rarr)
    return JsonResponse(rarr,safe=False)

def match_edit(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    sql="select isedit from Table_file where id="+str(id)
    cur.execute(sql)
    a=0
    for row in cur:
        a=row[0]
    if a==0: return JsonResponse(0,safe=False)
    else:
        sql="update Table_file set isedit=0 where id="+str(id)
        cur.execute(sql)
        cur.connection.commit()
        con.close()
        return JsonResponse(1,safe=False)


def end_edit(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    sql="update Table_file set isedit=1 where id="+str(id)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def get_groupnum(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    sql="select groupnum from Table_file where id="+str(id)
    cur.execute(sql)
    r=-1
    for row in cur:
        r=row[0]
    con.close()
    return JsonResponse(r,safe=False)