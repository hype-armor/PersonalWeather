/*!
 * jQuery UI Touch Punch 0.2.3
 *
 * Copyright 2011–2014, Dave Furfero
 * Dual licensed under the MIT or GPL Version 2 licenses.
 *
 * Depends:
 *  jquery.ui.widget.js
 *  jquery.ui.mouse.js
 */
!function(a){function f(a,b){if(!(a.originalEvent.touches.length>1)){a.preventDefault();var c=a.originalEvent.changedTouches[0],d=document.createEvent("MouseEvents");d.initMouseEvent(b,!0,!0,window,1,c.screenX,c.screenY,c.clientX,c.clientY,!1,!1,!1,!1,0,null),a.target.dispatchEvent(d)}}if(a.support.touch="ontouchend"in document,a.support.touch){var e,b=a.ui.mouse.prototype,c=b._mouseInit,d=b._mouseDestroy;b._touchStart=function(a){var b=this;!e&&b._mouseCapture(a.originalEvent.changedTouches[0])&&(e=!0,b._touchMoved=!1,f(a,"mouseover"),f(a,"mousemove"),f(a,"mousedown"))},b._touchMove=function(a){e&&(this._touchMoved=!0,f(a,"mousemove"))},b._touchEnd=function(a){e&&(f(a,"mouseup"),f(a,"mouseout"),this._touchMoved||f(a,"click"),e=!1)},b._mouseInit=function(){var b=this;b.element.bind({touchstart:a.proxy(b,"_touchStart"),touchmove:a.proxy(b,"_touchMove"),touchend:a.proxy(b,"_touchEnd")}),c.call(b)},b._mouseDestroy=function(){var b=this;b.element.unbind({touchstart:a.proxy(b,"_touchStart"),touchmove:a.proxy(b,"_touchMove"),touchend:a.proxy(b,"_touchEnd")}),d.call(b)}}}(jQuery);
</script><script>
var RADEG = 180.0 / Math.PI;
var DEGRAD = Math.PI / 180.0;
var INV360 = 1.0 / 360.0;
function daysSince2000Jan0( y, m, d){
 return (367*(y)-((7*((y)+(((m)+9)/12)))/4)+((275*(m))/9)+(d)-730530);
}
function sind(x){
	return Math.sin(x * DEGRAD);
}
function cosd(x){
	return Math.cos(x *DEGRAD);
}
function tand(x){
	return Math.tan(x * DEGRAD);
}
function atand(x){
	return Math.atan(x) * RADEG;
}    
function asind(x){
	return Math.asin(x) * RADEG;
}
function acosd(x){
	return Math.acos(x) * RADEG;
}
function atan2d(y, x){
	return Math.atan2(y, x) * RADEG;
}
function dayLength(year, month, day, lon, lat){
	return daylen(year, month, day, lon, lat, -35.0/60.0, 1);
}    
function dayCivilTwilightLength(year, month, day, lon, lat){
	return daylen(year, month, day, lon, lat, -6.0, 0);
}
function dayNauticalTwilightLength(year, month, day, lon, lat){
	return daylen(year, month, day, lon, lat, -12.0, 0);
}
function dayAstronomicalTwilightLength(year, month, day, lon, lat){
	return daylen(year, month, day, lon, lat, -18.0, 0);
}
function sunRiseSet(year, month, day, lon, lat){
	return sunriset(year, month, day, lon, lat, -35.0/60.0, 1);
}
function civilTwilight(year, month, day, lon, lat){
	 return sunriset(year, month, day, lon, lat, -6.0, 0);
}
function nauticalTwilight(year, month, day, lon, lat){
	return sunriset(year, month, day, lon, lat, -12.0, 0);
}
function astronomicalTwilight(year, month, day, lon, lat){
	return sunriset(year, month, day, lon, lat, -18.0, 0);
}
function sunriset(year, month, day, lon, lat, altit, upper_limb){
	// Compute d of 12h local mean solar time
	var d = daysSince2000Jan0(year,month,day) + 0.5 - (lon/360.0);
	
	// Compute local sidereal time of this moment 
	var sidtime = revolution(GMST0(d) + 180.0 + lon);
	
	// Compute Sun's RA + Decl at this moment 
	var res = sunRADec(d);
	var sRA = res[0];
	var sdec = res[1];
	var sr = res[2];
	
	//Compute time when Sun is at south - in hours UT 
	var tsouth = 12.0 - rev180(sidtime - sRA)/15.0;
	
	//Compute the Sun's apparent radius, degrees 
	var sradius = 0.2666 / sr;
	
	//Do correction to upper limb, if necessary 
	if (upper_limb) var altit = altit - sradius;
	
	// Compute the diurnal arc that the Sun traverses to reach 
	// the specified altitude altit: 
	
	var cost = (sind(altit) - sind(lat) * sind(sdec))/(cosd(lat) * cosd(sdec));

	if (cost >= 1.0){
	    var rc = -1 ;
	    var t = 0.0 ;           
	}    
	else if (cost <= -1.0){
	    var rc = +1 ;
	    var t = 12.0;          
    }
	else {
	    var t =  acosd(cost)/15.0  ;
	}  

	return [tsouth-t, tsouth+t]
}
function daylen(year, month, day, lon, lat, altit, upper_limb){
	// Compute d of 12h local mean solar time 
	var d = daysSince2000Jan0(year,month,day) + 0.5 - (lon/360.0);
		 
	// Compute obliquity of ecliptic (inclination of Earth's axis) 
	var obl_ecl = 23.4393 - 3.563E-7 * d;
	
	// Compute Sun's position 
	var res = sunpos(d);
	var slon = res[0];
	var sr = res[1];
	
	// Compute sine and cosine of Sun's declination 
	var sin_sdecl = sind(obl_ecl) * sind(slon);
	var cos_sdecl = Math.sqrt(1.0 - sin_sdecl * sin_sdecl);
	
	// Compute the Sun's apparent radius, degrees 
	var sradius = 0.2666 / sr;
	
	// Do correction to upper limb, if necessary 
	if (upper_limb) var altit = altit - sradius;

	    
	var cost = (sind(altit) - sind(lat) * sin_sdecl) / (cosd(lat) * cos_sdecl);
	if( cost >= 1.0) {
	    var t = 0.0 ;
	}
	else if(  cost <= -1.0){
	    var t = 24.0 ;      
	}
	else{
	    var t = (2.0/15.0) * acosd(cost);    
	}    
	return t
}

function sunpos(d){

	// Compute mean elements 
	var M =  revolution(356.0470 + 0.9856002585 * d);
	var w = 282.9404 + 4.70935E-5 * d;
	var e = 0.016709 - 1.151E-9 * d;
	
	// Compute true longitude and radius vector 
	var E = M + e * RADEG * sind(M) * (1.0 + e * cosd(M));
	var x = cosd(E) - e;
	var y = Math.sqrt(1.0 - e*e) * sind(E);
	var r = Math.sqrt(x*x + y*y) ;              
	var v = atan2d(y, x) ;                 
	var lon = v + w   ;                      
	if (lon >= 360.0){
	    lon = lon - 360.0   ;
	}
	    
	return [lon,r]
}

function sunRADec( d){
	// Compute Sun's ecliptical coordinates 
	var res =  sunpos(d);
	var lon = res[0];  
	var r = res[1] ;    
	
	// Compute ecliptic rectangular coordinates (z=0) 
	var x = r * cosd(lon);
	var y = r * sind(lon);
	
	// Compute obliquity of ecliptic (inclination of Earth's axis) 
	var obl_ecl = 23.4393 - 3.563E-7 * d;
	
	// Convert to equatorial rectangular coordinates - x is unchanged 
	var z = y * sind(obl_ecl);
	var y = y * cosd(obl_ecl);

	// Convert to spherical coordinates 
	var RA = atan2d(y, x)
	var dec = atan2d(z, Math.sqrt(x*x + y*y));

	return [RA, dec, r]
}
function zenith(year, month, day, hour,minute,lon, lat,timeshiftHr,jDay){
	var rdat=[];
	rdat=sunRADec(jDay);
	var ra=rdat[0];
	var dec=rdat[1];
	var r=rdat[2]; 

	// Compute d of 12h local mean solar time 
	var d = daysSince2000Jan0(year,month,day) + 0.5 - (lon/360.0);
		 
	// Compute obliquity of ecliptic (inclination of Earth's axis) 
	var obl_ecl = 23.4393 - 3.563E-7 * d;
	
	// Compute sine and cosine of Sun's declination 
	var sin_sdecl = sind(dec);
	var cos_sdecl = cosd(dec);

    // sin cos of lat
	var sin_lat=sind(lat);
	var cos_lat=cosd(lat);

	var sdat=[];
	sdat=sunRiseSet(year,month,day,lon,lat);
	var srise=sdat[0];
	var sset=sdat[1];
    var daylen=sset-srise;    
    var solarNoon=srise+0.5*daylen;   
    var solarNoon=solarNoon+timeshiftHr;
    var currentTime= hour +(minute/60.);   
    var deltaNoon=currentTime-solarNoon;   
    var degsHour=180./daylen;  
	var solarHourDeg=Math.abs(deltaNoon*degsHour);
	var cos_hr= cosd(solarHourDeg);
	 
	var n=sin_sdecl*sin_lat + cos_sdecl*cos_lat*cos_hr;
	if (n > 1 ) n=1
	 
	var zenith=acosd(n)
    return [solarHourDeg,zenith]
}

function revolution( x){
	return (x - 360.0 * Math.floor(x * INV360));
}
    
function rev180(x){
	return (x - 360.0 * Math.floor(x * INV360 + 0.5));
}

function GMST0( d){					
	var sidtim0 =  revolution((180.0 + 356.0470 + 282.9404) +(0.9856002585 + 4.70935E-5) * d);
	return sidtim0 
}
function solar_altitude(latitude, year, month, day){ 
        var N =  daysSince2000Jan0(year, month, day);
        var res =   sunRADec(N);
        var declination = res[1];
        var sr = res[2];
        var altitude = 90.0 - latitude  + declination;
        if (altitude > 90) altitude = 90 - (altitude-90);
        if (altitude < 0) altitude = 0;
        return altitude
}
    
  
    
function get_max_solar_flux( latitude, year, month, day){
         
		var edat=[];
		edat=equation_of_time(year, month, day, latitude);
        var fEot=edat[0];
		var fR0r=edat[1];
		var tDeclsc=[] 
		tDeclsc=edat[2];  
        var fSF = (tDeclsc[0]+tDeclsc[1])*fR0r

		 
		
        // In the case of a negative declinaison, solar flux is null
        if( fSF < 0) var fCoeff = 0;
        else var fCoeff =  -1.56e-12*Math.pow(fSF,4) + 5.972e-9*Math.pow(fSF,3) - 8.364e-6*Math.pow(fSF,2)  + 5.183e-3*fSF - 0.435;
       
        var fSFT = fSF * fCoeff ;

        if( fSFT < 0 ) var fSFT=0;

        return fSFT
}
function isleap(year){
 if( year%4==0 && year%10!=0) return true;
 return false
}
function equation_of_time( year, month, day, latitude){
        
        var nJulianDate = Julian(year, month, day);
         
        if(isleap(year)) var fDivide = 366.0;
        else var fDivide = 365.0;
		
         
        var fA = nJulianDate/fDivide*2*Math.PI;
        var fR0r = Solcons(fA)*0.1367e4;
        var fRdecl = 0.412*Math.cos((nJulianDate+10.0)*2.0*Math.PI/fDivide-Math.PI);
        var fDeclsc1 = sind(latitude)*Math.sin(fRdecl);
        var fDeclsc2 = cosd(latitude)*Math.cos(fRdecl);
        var tDeclsc = [fDeclsc1, fDeclsc2];
         
        var fEot = 0.002733 -7.343*Math.sin(fA)+ .5519*Math.cos(fA)  
               - 9.47*Math.sin(2.0*fA) - 3.02*Math.cos(2.0*fA)  
               - 0.3289*Math.sin(3.*fA) -0.07581*Math.cos(3.0*fA)  
               -0.1935*Math.sin(4.0*fA) -0.1245*Math.cos(4.0*fA);
         
        var fEot = fEot/60.0;
         
        var fEot = fEot*15*Math.PI/180.0;

        return [fEot, fR0r, tDeclsc]
}
function Solcons(dAlf){
        var dVar = 1.0/(1.0-9.464e-4*Math.sin(dAlf)-0.01671*Math.cos(dAlf)-  
                    + 1.489e-4*Math.cos(2.0*dAlf)-2.917e-5*Math.sin(3.0*dAlf)-  
                    + 3.438e-4*Math.pow(Math.cos(4.0*dAlf)),2);
        return dVar
}
function Julian( year, month, day){
         
        if(isleap(year)){ 
            var lMonth = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366];
		}
        else {
            var lMonth = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365];
		}

        var nJulian = lMonth[month-1] + day;
        return nJulian
}
