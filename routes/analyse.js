const express = require("express");
const youtubeController = require("../controller/youtube-controller");
const router = express.Router();

router.post("", (req, res) => {
  //console.log(req.body);
  const result = youtubeController.genUrl(req,res);
});
module.exports = router;
