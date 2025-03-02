import java.io.*;
import java.lang.*;
import java.util.*;
import java.math.*;


class AccessElements {
    
    public static int[] accessElements(int[] nums, int[] indices) {
        int[] result = new int[indices.length];
        for (int i = 0; i < indices.length; i++) {
            result[i] = nums[indices[i]];
        }
        return result;
    }
}

