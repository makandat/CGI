#!/usr/bin/env python3
#  Users クラスのテスト
import Users as users
import sys

if len(sys.argv) == 1 :
  print("Usage: test_Users.py testNo")
  exit(9)

testNo = int(sys.argv[1])

u = users.Users()

if testNo == 1 :
  # add_new
  u.add_new('test_user', '00000', 'テストユーザ')
elif testNo == 2 :
  # modify_info
  u.modify_info('test_user', 'テスト用')
elif testNo == 3 :
  # update_password
  u.update_password('test_user', '11111')
elif testNo == 4 :
  # encrypt_passwords
  u.encrypt_passwords()
elif testNo == 5 :
  # set_expired
  u.set_expired('test_user')
elif testNo == 6 :
  # userlist
  html = u.userlist(all=False, csv=False)
  print(html)
  csv = u.userlist(all=True, csv=True)
  print(csv)
elif testNo == 7 :
  # authorize
  print(u.authorize('test_user', '11111'))
  print(u.authorize('test_user', '00000'))
elif testNo == 0 :
  u.execute("DELETE FROM Users WHERE userid='test_user'")
  print("test_user が削除されました。")
else :
  print("不正な番号です。")

print("Done.")
