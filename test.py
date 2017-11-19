from crypt import Crypter
import rsa

#with open('public.pem', mode='rb') as pp:
#	keydata = pp.read()
#publickey = rsa.PublicKey.load_pkcs1_openssl_pem(keydata)
#print rsa.encrypt('ss', publickey)
#exit(1)

c=Crypter()
c.setSeed('6E 7E 4C 7D 4E 3F 7A 35 3B 21 2B 2E 5F 57 61 45')
plain='1Sun Nov 19 00:15:25 2017'
tmp='VWSj0AeDFgrCdYEAYsTH2np3q/VKoHy8n25RNOhyMp1W9NKhGnm0Mo+8ubJBfJRbBiK/PzSd2x1VjUxduFDnWuxqwnKfDSyThKZPmXWNU3ijyAizxooabm7+7walabaUjUmjaP3CnfX94ndlGt8sNszcM6iDg9NFlKChXYQDMPc='
#plain='{"buddy":{"1":{"hp":6,"sa":[],"panel1":null,"panel2":1,"panel3":1,"ss_gauge":100}},"supporter":{"supporter_ss_gauge":0},"beast":{"synchronization_count":0,"remain_active_skill_num":0},"score":{"general":[{"no":1,"val1":5,"val2":0,"val3":0,"val4":0,"val5":0},{"no":2,"val1":139,"val2":6,"val3":0,"val4":0,"val5":0},{"no":3,"val1":0,"val2":0,"val3":0,"val4":0,"val5":0}],"specific":[{"no":1,"val1":1,"val2":0,"val3":0,"val4":0,"val5":0}]},"log":{"action_time":0,"action_num":0,"buddy_damage":0,"enemy_damage":0,"fps":0,"supporter_ss_use_num":0,"all_enemy_info":[],"enemy_info":[],"continue_infos":[],"buddy_ab_use_num":{},"buddy_ss_use_num":{},"enemy_ab_use_num":{},"max_combo_num":0},"initChkResult":1,"session_key":"77814e41a24e4afcf83c31a62904c4f0"}'
#rsa,aes=tmp.split('_')
#print len(tmp),len(aes)


#crp= c.encrypt(plain)
#print '"%s"'%crp
#print '"%s"'%c.decrypt(tmp)
res= c.rsaEncryptText()
#if 'Pf3y009NkU8NV5gskWAEVkzpR' in res:
	#print res
#	exit(1)