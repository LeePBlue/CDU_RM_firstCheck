# 自动启动脚本

- ## 编辑启动脚本

  ```sh
  vim /lib/systemd/system/scurm.service
  ```

  ## 粘贴下列内容

  ```sh
  [Unit]
  Description=SCURM Auto-Load Script
  
  [Service]
  Type=simple
  TimeoutStartSec=5min
  ExecStart= /root/scurm/scurm.run
  ExecReload=/root/scurm/scurm.run
  ExecStop=  /root/scurm/scurm.ext
  Restart=always
  
  [Install]
  WantedBy=multi-user.target
  
  ```

- ## 放置启动脚本

  - #### 新建文件夹`mkdir /root/scurm`

  - #### 将文件拷贝到**`/root/scurm`**

    - **`scurm.ext`**
    - **`scurm.log`**
    - **`scurm.run`**

  - #### 修改启动脚本**`scurm.run`**

  - #### 修改结束脚本**`scurm.ext`**

  - #### 设置权限

    ```shell
    sudo chmod +x -R /root/scurm/
    ```

- ## 设置自动启动

  ```sh
  # 修改了scurm.service都需要执行
  sudo systemctl daemon-reload
  
  # 设置scurm.service为开机自启动
  sudo systemctl enable scurm
  ```

- ## 手动运行服务

  ```shell
  sudo systemctl start scurm
  ```

- ## 重启服务进程

  ```shell
  sudo systemctl restart scurm
  ```

- ## 查看运行状态

  ```shell
  sudo systemctl status scurm
  ```

- ## 查看PYTHON

  ```shell
  sudo ps -efa | grep python
  ```

- ## 结束运行状态

  ```shell
  sudo systemctl stop scurm
  ```

  