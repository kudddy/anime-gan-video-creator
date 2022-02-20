## anime-gan-video-creator
Сервис для генерации видео из кадров. Сервис получает из  очереди идентификаторы
файлов, загружает их, генерирует видео и отправляет его пользователю.

## Сборка проекта
сборка образа
```
docker build -t docker.io/kudddy/anime-gan-video-creator:release-01 .
```

загрузка образа
```
docker push docker.io/kudddy/anime-gan-video-creator:release-02
```

rolling update
```
kubectl set image deployments/anime-gan-video-creator animeganvideocreator=kudddy/anime-gan-video-creator:release-04
```

запуск контейнера
```
docker run docker.io/kudddy/anime-gan-video-creator:release-03
```