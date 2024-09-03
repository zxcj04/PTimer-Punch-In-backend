# 工讀生打卡系統 - 後端

## 簡介

使用 Flask 框架實作 RESTful API 設計。\
透過將驗證、使用者、打卡紀錄及匯出報表功能切分符合 SOLID 設計標準。\
在 API 端使用 Session id 來作為驗證手段，將短期 session 存在 Redis 記憶體資料庫中。\
將使用者資料及打卡紀錄存在 MongoDB 中。

## Contribution

### Prerequisite
- python
- pyenv (opt)
- pipenv

### Installation
`setup your .pypirc`
`mkdir .venv`
`pipenv install`

### Run ( Check Pipfile )
- dev
`pipenv run dev`

- prod test
`pipenv run prod`

