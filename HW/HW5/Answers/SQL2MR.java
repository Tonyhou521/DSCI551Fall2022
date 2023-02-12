import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class SQL2MR {

    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable> {

        private Text outputKey = new Text();
        private IntWritable outputValue = new IntWritable();

        public void map(Object key, Text value, Context context
        ) throws IOException, InterruptedException {

            //Getting input value and tokenize the value
            String[] toks = value.toString().split(",");

            //Setting tokens the correct values
            String carbodyTok = toks[6];
            String mpgTok = toks[toks.length - 2];
            String priceTok = toks[toks.length - 1];

            //converting the type of the variable mpgTok to mpg and priceTok to price
            int mpg = Integer.parseInt(mpgTok);
            float price = Float.parseFloat(priceTok);

            if (price >= 10000) {
                outputKey.set(carbodyTok);
                outputValue.set(mpg);
                context.write(outputKey, outputValue);
            }
        }
    }

    public static class IntSumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context
        ) throws IOException, InterruptedException {

            Map<String, List<Integer>> map = new HashMap<>();
            Iterator<IntWritable> iterator = values.iterator();
            List<Integer> mpglist = new ArrayList<>();

            while (iterator.hasNext()) {
                System.out.println(key);
                Integer mpg = iterator.next().get();
                System.out.println(mpg);
                mpglist.add(mpg);
            }
            if (mpglist.size() >= 5) {
                map.put(key.toString(), mpglist);
            }

            for (String k : map.keySet()) {
                int max = -1;
                List<Integer> mpgvals = map.get(k);
                for (Integer i : mpgvals) {
                    if (i > max) {
                        max = i;
                    }
                }
                context.write(new Text(k), new IntWritable(max));
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length < 2) {
            System.err.println("Usage: sql2mr <in> [<in>...] <out>");
            System.exit(2);
        }
        Job job = Job.getInstance(conf, "sql2mr");
        job.setJarByClass(SQL2MR.class);
        job.setMapperClass(TokenizerMapper.class);
        //job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        for (int i = 0; i < otherArgs.length - 1; ++i) {
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
        }
        FileOutputFormat.setOutputPath(job,
                new Path(otherArgs[otherArgs.length - 1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

