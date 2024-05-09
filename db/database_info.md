# Справка по устройству БД
## <sapn style="color:green">Таблицы:</span>
- Users
- MedSession
- Comment

```mermaid
classDiagram
      Users <|-- MedSession
      Users <|-- Comment
      class Users{
          id: int
          FK med_session_id: int
          FK comment_id: int
          first_name: str
          last_name: str
          patronymic: str | null
          login: str
          password: str
          email: str
          user_type: UserType
      }
      class MedSession{
          id: int
          FK user_id: int
          started_at: datetime
          finished_at: datetime
          exersise_type: ExerciseType
          max_angle: int
          avg_speed: int
      }
      class Comment{
          id: int
          text: str
          date: datetime
          exersise_type: ExerciseType
      }
      
     
```
