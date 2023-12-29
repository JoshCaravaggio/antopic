import axios from 'axios';

function parseErrorsIntoMessage(error) {
    var message = "\n";
    for (var key in error.response.data.errors) {
        message += key + " : " + error.response.data.errors[key].join(',') + "\n";
    }
    return message;
}

async function getTopic(id, accessToken) {    

    const config = {
        headers:{
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            Authorization: `Bearer ${accessToken}`,             
        }
      };
      const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/topics/${id}`, config)
      .catch(function (error) {
        if (error.response) {
          console.log(error.response.data);
          var message = parseErrorsIntoMessage(error);
          throw new Error(message);
        } else if (error.request) {
          console.log(error.request);
          throw new Error(error.request);
        }
      });
      console.log(response.data)
      return await response.data;
    }

async function getTopics(accessToken) {    

    const config = {
        headers:{
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            Authorization: `Bearer ${accessToken}`,             
        }
      };

    const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/topics`, config)
    .catch(function (error) {
      console.log(error)
        if (error.response) {
            console.log(error.response.data);
            var message = parseErrorsIntoMessage(error);
            throw new Error(message);
          } else if (error.request) {
            console.log(error.request);
            throw new Error(error.request.message);
          }
        });
        console.log(response.data)
    return await response.data;
}

async function createTopic(data,accessToken) {
    console.log("Creating review")
    const config = {
        headers:{
            'Content-Type' : 'application/json; charset=UTF-8',
            Authorization: `Bearer ${accessToken}`,             
        }
      };
    const response = await axios.post(`${process.env.VUE_APP_API_BASE_URL}/topics`,data, config)
    .catch(function (error) {
    if (error.response) {
        console.log(error.response.data);
        var message = parseErrorsIntoMessage(error);
        throw new Error(message);
      } else if (error.request) {
        console.log(error.request);
        throw new Error(error.request.message);
      }
    });
     return await response.data ;
}

async function createContent(data,accessToken) {
  console.log("Creating content");

  const config = {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  };

  if (data.type === "youtube") {
    config.headers["Content-Type"] = "application/json; charset=UTF-8";
  } else {
    const formData = new FormData();
    for (const key in data) {
      formData.append(key, data[key]);
    }
    data = formData;
  }

  const response = await axios.post(
    `${process.env.VUE_APP_API_BASE_URL}/contents`,
    data,
    config
  ).catch(function (error) {
  if (error.response) {
      console.log(error.response.data);
      var message = parseErrorsIntoMessage(error);
      throw new Error(message);
    } else if (error.request) {
      console.log(error.request);
      throw new Error(error.request.message);
    }
  });
   return await response.data ;
}

async function updateTopic(id, data, accessToken) {
    console.log(data)
    const config = {
        headers:{
            'Content-Type' : 'application/json; charset=UTF-8',
            Authorization: `Bearer ${accessToken}`,             
        }
      };
    const response = await axios.put(`${process.env.VUE_APP_API_BASE_URL}/topics/${id}`,data,config)
    .catch(function (error) {
        if (error.response) {
            console.log(error.response.data);
            var message = parseErrorsIntoMessage(error);
            throw new Error(message);        
          } else if (error.request) {
            console.log(error.request);
            throw new Error(error.request.message);
          }
        });
    return await response.data;


}

async function deleteTopic(id, accessToken) {
    const config = {
        headers:{
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            Authorization: `Bearer ${accessToken}`,             
        }
      };
    const response = await axios.delete(`${process.env.VUE_APP_API_BASE_URL}/topics/${id}`,config)
    .catch(function (error) {
        if (error.response) {
            console.log(error.response.data);
            var message = parseErrorsIntoMessage(error);
            throw new Error(message);
          } else if (error.request) {
            console.log(error.request);
            throw new Error(error.request.message);
          }
        });
    return await response.data;
}

async function deleteContent(id, accessToken) {
  const config = {
      headers:{
          'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
          Authorization: `Bearer ${accessToken}`,             
      }
    };
  const response = await axios.delete(`${process.env.VUE_APP_API_BASE_URL}/contents/${id}`,config)
  .catch(function (error) {
      if (error.response) {
          console.log(error.response.data);
          var message = parseErrorsIntoMessage(error);
          throw new Error(message);
        } else if (error.request) {
          console.log(error.request);
          throw new Error(error.request.message);
        }
      });
  return await response.data;
}

async function chat(topicId,question,history,accessToken) {    
    const config = {
        headers:{
            'Content-Type' : 'application/json; charset=UTF-8',
            Authorization: `Bearer ${accessToken}`,             
        }
      };

    const data =  JSON.stringify({
      question,
      history,
      topicId
    });

    const response = await axios.post(`${process.env.VUE_APP_API_BASE_URL}/chat`,data, config)
    .catch(function (error) {
    if (error.response) {
        console.log(error.response.data);
        var message = parseErrorsIntoMessage(error);
        throw new Error(message);
      } else if (error.request) {
        console.log(error.request);
        throw new Error(error.request.message);
      }
    });
    return await response.data;
}

async function getTopicPlaceholder(topicId,accessToken) {    
  const config = {
      headers:{
          'Content-Type' : 'application/json; charset=UTF-8',
          Authorization: `Bearer ${accessToken}`,             
      }
    };

  const data =  JSON.stringify({
    "question": "What is a question that would be asked about this content? Please provide an answer in the form of a question.",
    "history":[],
    topicId
  });

  const response = await axios.post(`${process.env.VUE_APP_API_BASE_URL}/chat`,data, config)
  .catch(function (error) {
  if (error.response) {
      console.log(error.response.data);
      var message = parseErrorsIntoMessage(error);
      throw new Error(message);
    } else if (error.request) {
      console.log(error.request);
      throw new Error(error.request.message);
    }
  });
  return await response.data.answer;
}

export default {
        getTopic, 
        getTopics,
        updateTopic,
        createTopic,
        deleteTopic,
        createContent,
        deleteContent,
        chat,
        getTopicPlaceholder
}