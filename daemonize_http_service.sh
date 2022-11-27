
pm2 stop christmas_tree
pm2 delete christmas_tree
pm2 start "sudo python server.py" --name christmas_tree
pm2 save
pm2 logs

