const express = require("express");
const path = require("path");
const facebook = require("./routes/facebook");
const youtube = require("./routes/youtube");
const insta = require("./routes/insta");
const analyse  = require("./routes/analyse");
const app = express();
const PORT = 3000;
var hbs = require("hbs");
hbs.registerPartials(__dirname + "/views/partials");
app.listen(PORT, () => {
  console.log(`Listening at ${PORT}`);
});
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.set("views", path.join(__dirname, "./templates/pages"));
app.set("view engine", "hbs");
app.use(express.static(path.join(__dirname, "public")));
app.get("/",(req,res)=>{
    res.render("main");
});
app.use("/facebook",facebook);
app.use("/youtube",youtube);
app.use("/insta", insta);
app.use("/analyse",analyse);