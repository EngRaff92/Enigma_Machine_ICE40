//! Reflector RTL module:
//!     -> no clock provided is fully combo
//!     -> internal LUT initialization is only based on IMAGE
//!     -> API are provided to peek poke the LUT

`timescale 1ns/1ns

module reflector #(
    parameter FILE          = "",
    parameter ALPHABET_LEN  = 32'd26,
    parameter PORTLEN       = 32'd5,
    parameter STATE         = 32'd0
) (
    /** The main port length is defined based on the Alphabet len */
    input logic [PORTLEN-1:0]   input_letter,
    /** The Reflector operates only if the currect flows through we use a CS to mimic */
    input logic                 re_cs_n,
    /** The main port length is defined based on the Alphabet len */
    output logic [PORTLEN-1:0]  output_letter,
    /** In case of not allowed Char we return an error so make sure to use only supported char */
    output  logic               error
);

`ifndef SYNTH
    /** PARAM CHECK only allowed outside SYNTH and WITH no FORMAL*/
    initial begin
        if(PORTLEN != $clog2(ALPHABET_LEN))
            $error("PORTLEN is not computed as log 2 of Alphabet len, not enough bits");
    end
`endif 

    /** LOAD LUT */
    initial begin
        /* verilator lint_off WIDTH */
        if(FILE != "")  $readmemb(FILE,lut_reflect);
        /* verilator lint_off WIDTH */
        else            $display("Filename for Inital LUT loading not provided");
    end

    /** Let's model the Reflector as a LUT/MEMORY */
    logic [PORTLEN-1:0] lut_reflect[ALPHABET_LEN-1:0];

    /** The error mechanims is handled during the follwoing scenarios:
    1. If the input letter exceeds the allowd Alphabet Len */
    assign error = (input_letter >= ALPHABET_LEN);

    /** Anytime a new letter is sent we look for the address into the LUT along with and we return the associated */
    logic [PORTLEN-1:0] LUT_OUT;
    always_comb begin: reflect_process
        LUT_OUT = lut_reflect[input_letter];
        if((~error) & (~re_cs_n))
            output_letter   = LUT_OUT;
        else
            output_letter   = 'h0;
    end

`ifdef COCOTB_SIM
    /** API */
    /* setReflector internal function used to plug a value into the LUT (no error if plugged):
        @param: char value of the lut
        @param: value value to be set
    */
    function void setReflector(input logic [PORTLEN-1:0] char, value);
        lut_reflect[char] = value;
    endfunction 

    /* reflect internal function used to get the reflected a value into the LUT:
        @param: char_in value of the lut
        @return: value reflected
    */
    function int reflect(input logic [PORTLEN-1:0] char_in);
        return lut_reflect[char_in];
    endfunction 

    /* load_lut internal task to load the LUT:
        @param: file_hex path to the file hex to be loaded, can be .hex or .mem extension
    */
    task load_lut(input string file_hex);
        $display("Loading ./Reflector.bin");
        $readmemb(file_hex,lut_reflect);
    endtask

    // Standard VCD
    initial begin
      $dumpfile("dump.vcd");
      $dumpvars(0);
    end
`endif
endmodule // Reflector