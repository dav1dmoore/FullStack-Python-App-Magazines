
function gcf(x, y) {
  if(x>y){
    if(x%y == 0){
        console.log(y)
        return y
    } else {
    x = x - y
    }
  } else {
    if(y%x == 0){
        console.log(x)
        return x
    } else {
    y = y - x
    }
  }
  console.log(x, y)
  if(x == y){
    console.log(x)
    return x
  } else {
    gcf(x,y)
  }
    // Write your solution here!
  }
  
  gcf(9,81)



  <!-- <h1>Manage My magazines</h1>
  <table class="">
      <thead>
      <tr>
        <th>Name</th>
        <th>Date Planted</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
          {% for magazine in magazines %}
          <tr>
            <td>{{magazine.name}}</td>
            <td>
              <a href="/edit_magazine/{{magazine.id}}">Edit</a> | 
                <a href="/delete_magazine/{{magazine.id}}"> Delete </a></p>
            </td>
          </tr>
          {% endfor %}
      </tbody>
    </table> -->



    magazine = Magazine.get_magazine_to_edit(data)
    print(magazine)


    @classmethod
    def get_magazine_to_edit(cls, data):
        query = "SELECT * FROM magazines WHERE magazines.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result[0]

        SELECT COUNT(subscription.user_id) AS 'subscription', magazines.name, first_name, last_name  FROM magazines JOIN users ON users.id = magazines.user_id LEFT JOIN subscription ON subscription.magazine_id = magazines.id GROUP BY magazines.name