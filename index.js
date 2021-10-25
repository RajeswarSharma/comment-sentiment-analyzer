const express = require("express");
const path = require("path");
const facebook = require("./routes/facebook");
const youtube = require("./routes/youtube");
const app = express();
const PORT = 3000;

app.listen(PORT, () => {
  console.log(`Listening at ${PORT}`);
});
app.set("views", path.join(__dirname, "./templates/pages"));
app.set("view engine", "hbs");
app.use(express.static(path.join(__dirname, "public")));
app.get("/",(req,res)=>{
    res.render("main");
});
app.use("/facebook",facebook);
app.use("/youtube",youtube);