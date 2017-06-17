
sudo rm /etc/nginx/sites-enabled/default
sudo cp $PYTHONPATH/operation_service/conf/operation_service_nginx.conf /etc/nginx/sites-enabled/
pkill gunicorn
cd $PYTHONPATH/operation_service/conf
echo $PWD
gunicorn -c gunicorn.py service_app:app
sudo service nginx restart
