import java.io.*;
import java.lang.*;
import java.util.*;
import java.math.*;

class AddConsecutiveNums {
    
    public static int[] addConsecutiveNums(int[] nums) {
        if (nums.length < 2) {
            return new int[0];
        }
        int[] result = new int[nums.length - 1];
        for (int i = 0; i < nums.length - 1; i++) {
            result[i] = nums[i] + nums[i + 1];
        }
        return result;
    }
}

