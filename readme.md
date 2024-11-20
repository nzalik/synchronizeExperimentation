








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
        train/load2/nantes/hyperthreading/128/linear/3nodes/linear/11-11-2024/

        Experimentation avec les profils load1 et load2 dont les configurations de profil
        limites 
        duration=300
            max_req=50
            min_req=10 | 20
            nb_files_per_func=1
            nb_f_offset=2
    cpu_step 120s
        locust/nantes/train/16-11-2024/train_load_100profile_called_sequentially injection en utilisant les profils dont la limitation est à 100, etc

        locust/nantes/train/19-11-2024/load1profile_with_deep_locustfile_extended lancer avec deep_load_generator_train.py comme scenarios de test
        locust/nantes/train/19-11-2024/load2profile_with_deep_locustfile_extended 


    2. Teastore
cpu_step 120
        locust/previous_data/low_10/nantes/hyperthreading/128/linear/3nodes/linear/07-11-2024/ | locust/previous_data/load1/nantes/hyperthreading/128/linear/3nodes/linear/07-11-2024 is extension of low_10
        locust/previous_data/low_20/nantes/hyperthreading/128/linear/3nodes/linear/07-11-2024
        Teastore 1cpu | 5gb load1 et load2

        locust/nantes/teastore/load1|load2/hyperthreading/12-11-2024/ : data with a constant load of 10 req/s for min 
        followed by the collection of data for different profiles

        locust/nantes/teastore/load1_sequential_injection : data after only one warmup, and profile usage and data collection
        no limit on cpu and pod 
        locust/nantes/teastore/load1_sequential_injection_cpu_limit
        locust/nantes/teastore/load2_sequential_injection_cpu_limit for injection with cpu limit to 1 
        
        

        



