#!/usr/bin/env python  
#coding=utf-8  
import amqplib.client_0_8 as amqp  
import time
import ftpupdown
import qz
def showmsg(msg):  
    bod = str(msg.body,'utf-8')
    writename = "/home/wanli/src/pdftest/images/"+bod.split('/')[1]
    print(bod)
    print(writename)
    try:
        ftpupdown.ftp_down(bod,writename)
    except:
        print('continue')
    filename = qz.changgepdf(writename)
    ftpupdown.ftp_up(filename,"/pypdf/"+bod)
    # time.sleep(3)
    msg.channel.basic_ack(msg.delivery_tag)  
    if msg.body == 'quit':  
        msg.channel.basic_cancel(msg.consumer_tag)  
def main():  
    server = {'host':'192.168.0.251', 'userid':'guest', 'password':'guest', 'ssl':False}  
    x_name = ''  
    q_name = 'changepdf'  
    conn = amqp.Connection( server['host'],userid=server['userid'],password=server['password'])
    ch = conn.channel()  
    ch.access_request('/data', active=True, read=True)  
    ch.basic_qos(prefetch_count=1,prefetch_size=0,a_global=False)
    #ch.exchange_declare(exchange=x_name, type='fanout', durable=True, auto_delete=False)  
    ch.queue_declare(queue=q_name, durable=True, exclusive=False, auto_delete=False)  
    #ch.queue_bind(queue=q_name, exchange='')  
    ch.basic_consume(q_name, callback=showmsg)  
    while ch.callbacks:  
        ch.wait()  
    ch.close()  
    conn.close()  
if __name__ == '__main__':  
    main()