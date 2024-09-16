-- http_calls_minimal.lua

-- Configuration de base
local BASE_URL = "172.16.192.22:30081"
--local BASE_URL = "http://your-nginx-url"  -- Remplacez par votre URL
local users = 100  -- Nombre d'utilisateurs simulés
local wait_time = {1, 3}  -- Intervalle d'attente entre les requêtes

-- Fonction pour simuler un utilisateur
function simulate_user(user_id)
    while true do
        -- Simuler un post
        local post_text = "Post from user " .. user_id
        local post_data = "user_id=" .. user_id .. "&text=" .. post_text

        -- Envoi de la requête POST pour composer un post
        http.post(BASE_URL .. "/wrk2-api/post/compose", post_data)

        -- Simuler une lecture de la timeline d'accueil
        local start = math.random(0, 100)
        local stop = start + 10
        http.get(BASE_URL .. "/wrk2-api/home-timeline/read?start=" .. start .. "&stop=" .. stop .. "&user_id=" .. user_id)

        -- Simuler une lecture de la timeline d'un utilisateur ami
        local friend_id = math.random(1, users)  -- Remplacez par la logique pour choisir un ami
        http.get(BASE_URL .. "/wrk2-api/user-timeline/read?start=" .. start .. "&stop=" .. stop .. "&user_id=" .. friend_id)

        -- Attendre un certain temps
        local wait = math.random(wait_time[1], wait_time[2])
        os.execute("sleep " .. wait)
    end
end

-- Lancer la simulation pour plusieurs utilisateurs
for user_id = 1, users do
    simulate_user(user_id)  -- Vous pouvez utiliser des threads pour une simulation parallèle
end