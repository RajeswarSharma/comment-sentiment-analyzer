const url = require("url");
const request = require("request");
const axios = require("axios");

const sender = (res,comments) => {
  axios
    .post("http://192.168.1.4:5000/predict",comments)
    .then((data) => {
      console.log("recived data");
      console.log(data.data);
      res.json({ data: data.data });
    })
    .catch((err) => {
      console.log(err.message);
    });
};
function parseUrl(recivedUrl) {
  const url_parts = url.parse(recivedUrl, true);
  const fixedUrl = JSON.parse(JSON.stringify(url_parts));
  return {
    v: fixedUrl.query.v,
    ab_channel: fixedUrl.query.ab_channel,
  };
}
function getComments(comments) {
  let result = [];
  for (let i in comments) {
    result.push(comments[i].snippet.topLevelComment.snippet.textDisplay);
  }
  return result;
}

exports.genUrl = async (req, res) => {
  const result = parseUrl(req.body.link);
  const APIURLRaw = `https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=200&order=orderUnspecified&key=AIzaSyBwjPJaqpM9EQEtjeVvCTecEf66sBpnMPM&videoId=${result.v}`;
  await request(APIURLRaw, async (err, response, body) => {
    const comments = JSON.parse(body);
    const processedComments = getComments(comments.items);
    sender(res,processedComments);
  });
};
