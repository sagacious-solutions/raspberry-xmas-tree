
pm2 stop alexa_service
pm2 delete alexa_service
pm2 start "sudo python alexa_service.py" --name alexa_service
pm2 save
pm2 logs

