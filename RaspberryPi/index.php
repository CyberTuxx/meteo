<!DOCTYPE html>

<head>
    <meta charset="utf-8"/>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>RaspPi Metéo</title>
</head>
<body>
<?php
require_once('MeteoDAO.php');
require_once('./config/configuration.php');
$meteoDAO = new MeteoDAO();
if(isset($_GET['order'])) {
    $crois = "desc";
    $order = $_GET['order'];
    if($order == "Temperature"){
        $order = "temp";
    }elseif ($order == "Humidité"){
        $order = "humidity";
    }elseif($order == "Pression"){
        $order = "pression";
    }elseif($order == "Date"){
        $order = "date";
    }else{
        $order = "date";
    }
    if(isset($_GET['crois'])){
        if($_GET['crois'] == "Croissant"){
            $crois = "";
        }else{
            $crois = "desc";
        }
    }
    $meteo = $meteoDAO->getMeteo($order, $crois);
}else{
    $meteo = $meteoDAO->getMeteo("date", "desc");
}
if(isset($_GET['date'])){
    $meteoDAO->removeMeteo($_GET['date']);
}

if(isset($_GET['maxvalue'])){
    $maxvalue = $_GET['maxvalue'];
    if($maxvalue == "All"){
        $maxvalue = $meteoDAO->countMeteo();
    }
}else {
    $maxvalue = 20;
}

?>
<table class="realtime">
    <td><?php
        $res = $meteoDAO->getMeteoDirect();
		foreach ($res as $resultat){
			echo $resultat->getTemp();
		}
        echo "°C"?>
    </td>
    <td><?php
        foreach ($res as $resultat){
			echo $resultat->getHumidity();
		}
        echo " %"?>
    </td>
    <td><?php
        foreach ($res as $resultat){
			echo $resultat->getPression();
		}
        echo " hPa"?>
</table>
<table class="option"><tr><td>
<form index.php?maxvalue="$maxvalue" class="maxvalue">
    <select name="maxvalue">
        <option>20</option>
        <option>40</option>
        <option>80</option>
        <option>All</option>
    </select>
    <button type="submit">Afficher</button>
</form>
        </td><td>
<form index.php?save="$save=$save" class="save">
    <button type="submit" name="save" value="ok"><?php
        if(isset($_GET['save'])){
            $meteoDAO->save();
			echo "Sauvegarder";
        }else{
			echo "Sauvegarder";
		}
        ?></button>
</form>
        </td></tr>

<table>
    <tr class="tri">
        <form index.php?order="$order=$order?$crois=$crois">
            <?php if(isset($_GET['crois'])){
                if($_GET['crois'] == "Croissant"){?>
                    <input type="hidden" name="crois" value="Decroissant"><?php
                }else{?>
                    <input type="hidden" name="crois" value="Croissant"><?php
                }
            }else{?>
                <input type="hidden" name="crois" value="Croissant"><?php
            }?>
            <td><p><button type="submit" name="order" value="Temperature">Temperature</button></p></td>
            <td><p><button type="submit" name="order" value="Humidité">Humidité</button></p></td>
            <td><p><button type="submit" name="order" value="Pression">Pression</button></p></td>
            <td><p><button type="submit" name="order" value="Date">Date</button></p></td>
        </form>
    </tr>
<?php
$i = 0;
foreach ($meteo as $table){
    $i = $i + 1;?>
    <tr>
        <form index.php?date="$date=$date">
            <td><?php echo $table->getTemp(); echo "°C"?></td>
            <td><?php echo $table->getHumidity(); echo " %"?></td>
            <td><?php echo $table->getPression();echo " hPa"?></td>
            <td><button class="delete" type="submit" name="date" value="<?php echo $table->getDate()?>"><?php echo date('d/m/y H:i', strtotime($table->getDate()));?></button></td>
        </form>
    </tr><?php
    if($i >= $maxvalue){
        break;
    }
}?></table>
</body>
<?php
?>
