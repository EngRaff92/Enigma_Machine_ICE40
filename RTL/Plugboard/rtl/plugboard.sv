//! Plugboard RTL module:
//! -> no clock provided is fully combo
//! -> internal LUT initialization is only based on IMAGE
//! -> API are provided to peek poke the LUT
//! -> If no file is provided the PLUGBOARD will be self plugged with no plugs: not supported

`timescale 1ns/1ns

module plugboard #(
    parameter SELFPLUGGED   = 32'd0, 
    parameter ALPHABET_LEN  = 32'd26,
    parameter PORTLEN       = 32'd5
) (
    //! The main port length is defined based on the Alphabet len
    input logic [PORTLEN-1:0]   input_letter,
    //! The plugboard operates only if the currect flows through we use a CS to mimic
    input logic                 pb_cs_n,
    //! The main port length is defined based on the Alphabet len
    output logic [PORTLEN-1:0]  output_letter,
    //! In case of not allowed Char we return an error so make sure to use only
    //! supported char
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
        $readmemb("/Volumes/My_Data/MY_SYSTEMVERILOG_UVM_PROJECTS/ENIGMA_ICE40/RTL/Plugboard/collateral/plugboard.bin",lut_plug);
    end


    /** Let's model the Plugboard as a LUT/MEMORY: 1 additional bit is set to figure if plugged.
        An error is fired if we try to plug a plugged value */
    logic [PORTLEN:0] lut_plug[ALPHABET_LEN-1:0];

    /** Anytime a new letter is sent we look for the address into the LUT along with
        the connection bit (PORTLEN+1 bit) if connected we return the associated
        letter otherwise we return itself. If the connected output is equal to the input
        letter we fire an error*/
    logic [PORTLEN-1:0] LUT_OUT;
    logic               plugged;
    logic [PORTLEN:0]   Rvalue;
    always_comb begin: lut_read
        if(overflow) begin
            Rvalue  = 0;
            plugged = 0;
            LUT_OUT = 0; 
        end else begin
            Rvalue  = lut_plug[input_letter];
            plugged = Rvalue[PORTLEN];
            LUT_OUT = Rvalue[PORTLEN-1:0];
        end
    end

    /** The error mechanims is handled during the follwoing scenarios:
        1. If the input letter exceeds the allowd Alphabet Len
        2. If a Letter is Plugged to itself (which is not physically possible*/
    logic overflow;
    /* verilator lint_off WIDTH */
    assign overflow = (input_letter >= ALPHABET_LEN);
    /* verilator lint_on WIDTH */
    assign error    = (((plugged == 1) & (input_letter == LUT_OUT)) | overflow);

    /** Driver the output letter is kept low if an error occurs while CS_N is active, an error will prevent the
        consumer consuming the 0 value*/
    always_comb begin: output_driver
        if((~error) & (~pb_cs_n))
            output_letter   = plugged ? LUT_OUT : input_letter;
        else
            output_letter   = 'h0;
    end

`ifdef COCOTB_SIM
    /** API */
    /* Plug internal function used to plug a value into the LUT (no error if plugged):
        @param: char value of the lut
        @param: value value to be plugged
    */
    function void plug(input logic [PORTLEN-1:0] char, plug);
        lut_plug[char] = plug;
    endfunction 
    /* get_plug internal function used to get the plugged a value into the LUT:
        @param: char_in value of the lut
        @return: value plugged
    */
    function int get_plug(input logic [PORTLEN-1:0] char_in);
        return lut_plug[char_in];
    endfunction 

    /* load_lut internal task to load the LUT:
        @param: file_hex path to the file hex to be loaded, can be .hex or .mem extension
    */
    task load_lut(input string file_hex);
        $display("Loading ./plugboard.bin");
        $readmemb(file_hex,lut_plug);
    endtask

    // Standard VCD
    initial begin
      $dumpfile("dump.vcd");
      $dumpvars(0);
    end
`endif
endmodule // plugboard