








# Deploy istio

---> Navigate to /mesh

---> Use the istio.sh to deploy istio and others services (Prometheus, Grafana, ...)

# Deploy linkerd

/bin/bash ./Generator/organized_central_unit.sh ./conf/teastore.conf

pip3 install -r requirements.txt

python3 -m venv myenv

source myenv/bin/activate

 /bin/bash ./Generator/train_central_unit.sh ./conf/train.conf

# DATA COLLECTION 

    1. Data about train ticket
      train/load1/nantes/hyperthreading/128/linear/3nodes/linear/11-11-2024/
        train/load1/nantes/hyperthreading/128/linear/3nodes/linear/11-11-2024/

        Experimentation avec les profils load1 et load2 dont les configurations de profil
        limites 
        duration=300
            max_req=50
            min_req=10 | 20
            nb_files_per_func=1
            nb_f_offset=2

    2. Teastore
        locust/previous_data/low_10/nantes/hyperthreading/128/linear/3nodes/linear/07-11-2024/ | locust/previous_data/load1/nantes/hyperthreading/128/linear/3nodes/linear/07-11-2024 is extension of low_10
        locust/previous_data/low_20/nantes/hyperthreading/128/linear/3nodes/linear/07-11-2024
        Teastore 1cpu | 5gb load1 et load2

        



