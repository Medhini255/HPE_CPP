- **Step1** : 
    ```bash
    ls -ld /home/<root user>/<project directory>/<service directory>

- **Step2** : 
    ```bash
    ls -ld /home/<root user> /home/<root user>/<project directory>

- **Step3** :
    ```bash
    sudo chmod o+rx /home/<root user> /home/<root user>/<project directory>

- **Step4** : 
    ```bash
    sudo -u postgres psql ====> Now works correctly
