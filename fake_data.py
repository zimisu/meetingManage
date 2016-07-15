# -*-coding:utf-8-*-
__author__ = 'kanchan'
import pymongo

client = pymongo.MongoClient()
db = client.chidao

db.meeting.insert_one({
    "meetingid": "0",
    "title": "test title0",
    "content": "test content0",
    "place": "test0",
    "start_check": 1,
    "punishment_id": "1",
    'timestamp': 1451577600.0,
    "attendee": [{"openid": "oiNduwH4BC3nKrSfd6HQRMsKRY88",
                  "status": "not checked",
                  "timestamp": 1468484346},
                 {"openid": "oiNduwPswzDqXDi0CNxpeSbZfutg",
                  "status": "not checked",
                  "timestamp": 1460484346}
    ]})

db.meeting.insert_one({
    "meetingid": "1",
    "title": "test title1",
    "content": "test content1",
    "place": "test1",
    "start_check": 1,
    "punishment_id": "1",
    'timestamp': 1451581261.0,
    "attendee": [{"openid": "oiNduwH4BC3nKrSfd6HQRMsKRY88",
                  "status": "not checked",
                  "timestamp": 1368484346},
                 {"openid": "oiNduwPswzDqXDi0CNxpeSbZfutg",
                  "status": "not checked",
                  "timestamp": 0}
    ]})

db.meeting.insert_one({
    "meetingid": "2",
    "title": "test title2",
    "content": "test content2",
    "place": "test2",
    "start_check": 1,
    "punishment_id": "1",
    'timestamp': 1551581261.0,
    "attendee": [{"openid": "oiNduwH4BC3nKrSfd6HQRMsKRY88",
                  "status": "not checked",
                  "timestamp": 1368484346},
                 {"openid": "oiNduwPswzDqXDi0CNxpeSbZfutg",
                  "status": "not checked",
                  "timestamp": 0},
                 {"openid": "oiNduwOAu6wqjuxzEBNduF-cwXs0m",
                  "status": "not checked",
                  "timestamp": 0}

    ]})

db.meeting.insert_one({
    "meetingid": "3",
    "title": "test title3",
    "content": "test content3",
    "place": "test3",
    "start_check": 1,
    "punishment_id": "2",
    'timestamp': 1551581261.0,
    "attendee": [
                 {"openid": "oiNduwOAu6wqjuxzEBNduF-cwXs0m",
                  "status": "not checked",
                  "timestamp": 0}

    ]})

access_token = 'oLha1CgF2Dbxp8yoRqE_QmTx3F7VW_AlE0m91lwbSRKP2Gk6O2IhT-cI_jtei-pzLmau8r9FLyc9DbjNTfg20HGTTBPM_jrr3upUbMKfD58t7Dgci4SlCVI2Pgsk_ZFFIOYaAIADJT'