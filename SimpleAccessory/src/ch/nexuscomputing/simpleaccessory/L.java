/**
 *
 * @author      Manuel Di Cerbo
 * @copyright   Copyright (c) 2013, Manuel Di Cerbo, Nexus-Computing GmbH
 *
 * This file is part of SimpleAccessory.
 *
 * SimpleAccessory is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License version 2, as published by the
 * Free Software Foundation.
 *
 * You may NOT assume that you can use any other version of the GPL.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
 *
 * You should have received a copy of the GNU General Public License along with
 * this program; if not, write to:
 *
 *      Free Software Foundation, Inc.
 *      51 Franklin St, Fifth Floor
 *      Boston, MA  02110-1301  USA
 *
 * The license for this software can also likely be found here:
 * http://www.gnu.org/licenses/gpl-2.0.html
 */

package ch.nexuscomputing.simpleaccessory;

import android.util.Log;


public class L {
	private static final boolean SHUT_UP = false;

	public static void d(Object o){
		if(BuildConfig.DEBUG && !SHUT_UP)
			Log.d(">==< SimpleAccessory >==<", String.valueOf(o));
	}
	public static void d(String s, Object ... args){
		if(BuildConfig.DEBUG && !SHUT_UP)
			Log.d(">==< SimpleAccessory >==<", String.format(s,args));
	}
	
	public static void e(Object o){
		if(BuildConfig.DEBUG && !SHUT_UP)
			Log.e(">==< SimpleAccessory >==<", String.valueOf(o));
	}
}




